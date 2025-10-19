
import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import importlib.util
from scipy import stats
import matplotlib.pyplot as plt

# Path to the aligned data CSV
DATA_PATH = os.path.join("data", "gold_sp500_aligned.csv")
HIST_JSON_PATH = "histprices.json"

# US Recession periods (NBER dates from 1971 onwards)
RECESSION_PERIODS = [
    ("1973-11-01", "1975-03-31"),  # 1973-75 Oil Crisis Recession
    ("1980-01-01", "1980-07-31"),  # 1980 Recession
    ("1981-07-01", "1982-11-30"),  # 1981-82 Early 1980s Recession
    ("1990-07-01", "1991-03-31"),  # 1990-91 Gulf War Recession
    ("2001-03-01", "2001-11-30"),  # 2001 Dot-com Recession
    ("2007-12-01", "2009-06-30"),  # 2007-09 Great Recession
    ("2020-02-01", "2020-04-30"),  # 2020 COVID-19 Recession
]

def add_recession_shading(ax, start_date, end_date):
    """
    Add grey shading for US recession periods to a matplotlib axis.
    
    Args:
        ax: matplotlib axis object
        start_date: pd.Timestamp - start of the visible date range
        end_date: pd.Timestamp - end of the visible date range
    """
    for recession_start, recession_end in RECESSION_PERIODS:
        rec_start = pd.Timestamp(recession_start)
        rec_end = pd.Timestamp(recession_end)
        
        # Only shade if recession overlaps with visible date range
        if rec_end >= start_date and rec_start <= end_date:
            ax.axvspan(rec_start, rec_end, alpha=0.2, color='gray', zorder=0)


# Check if CSV exists, if not, run enhanced preprocessing
if not os.path.exists(DATA_PATH):
    st.info("Fetching historical data... This may take a moment.")
    spec = importlib.util.spec_from_file_location("preprocess_1971", os.path.join("src", "preprocess_1971.py"))
    preprocess = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preprocess)
    preprocess.main()
    st.success("Data loaded successfully!")

st.title("Gold vs S&P 500: Historical Comparison (1971-Present)")
st.markdown("""
Compare gold and S&P 500 performance since **1971** - the year the US left the gold standard.

This analysis uses:
- **Historical monthly gold prices** from 1971-present
- **S&P 500 index data** from Yahoo Finance (1971-present)
""")

# Sidebar for data settings
st.sidebar.header("📊 Analysis Settings")

# Load the data
@st.cache_data
def load_data():
    """Load and cache the dataset."""
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    
    # Filter to 1971 onwards
    df = df[df['date'] >= '1971-01-01']
    df = df.dropna()
    df = df.sort_values('date').reset_index(drop=True)
    
    return df

df = load_data()

st.sidebar.write(f"**Data Range:** {df['date'].min().date()} to {df['date'].max().date()}")
st.sidebar.write(f"**Total Records:** {len(df):,}")
st.sidebar.write(f"**Frequency:** {'Monthly' if len(df) < 1000 else 'Daily'}")

# Date range selector
st.sidebar.header("📅 Date Range")

# Get min/max dates
min_date = df["date"].min().date()
max_date = df["date"].max().date()

# Add preset date ranges
preset_ranges = st.sidebar.selectbox(
    "Preset Ranges:",
    [
        "Custom",
        "Last 1 Year", 
        "Last 5 Years",
        "Last 10 Years",
        "Last 20 Years",
        "Since 2000",
        "Since 1980",
        "Since 1971 (All Data)"
    ]
)

# Calculate date range based on preset
if preset_ranges == "Last 1 Year":
    start_preset = max_date.replace(year=max_date.year - 1) if max_date.year > min_date.year else min_date
    end_preset = max_date
elif preset_ranges == "Last 5 Years":
    start_preset = max_date.replace(year=max_date.year - 5) if max_date.year - 5 >= min_date.year else min_date
    end_preset = max_date
elif preset_ranges == "Last 10 Years":
    start_preset = max_date.replace(year=max_date.year - 10) if max_date.year - 10 >= min_date.year else min_date
    end_preset = max_date
elif preset_ranges == "Last 20 Years":
    start_preset = max_date.replace(year=max_date.year - 20) if max_date.year - 20 >= min_date.year else min_date
    end_preset = max_date
elif preset_ranges == "Since 2000":
    start_preset = datetime(2000, 1, 1).date() if datetime(2000, 1, 1).date() >= min_date else min_date
    end_preset = max_date
elif preset_ranges == "Since 1980":
    start_preset = datetime(1980, 1, 1).date() if datetime(1980, 1, 1).date() >= min_date else min_date
    end_preset = max_date
elif preset_ranges == "Since 1971 (All Data)":
    start_preset = min_date
    end_preset = max_date
else:  # Custom
    start_preset = min_date
    end_preset = max_date

# Show custom date selector if "Custom" is selected
if preset_ranges == "Custom":
    st.sidebar.write("**Select Custom Date Range:**")
    
    # Calendar-style date inputs
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date_input = st.date_input(
            "Start Date",
            value=start_preset,
            min_value=min_date,
            max_value=max_date,
            key="start_date"
        )
    with col2:
        end_date_input = st.date_input(
            "End Date",
            value=end_preset,
            min_value=min_date,
            max_value=max_date,
            key="end_date"
        )
    
    # Validate date range
    if start_date_input > end_date_input:
        st.sidebar.error("⚠️ Start date must be before end date!")
        start_date_input = min_date
        end_date_input = max_date
    
    date_range = (start_date_input, end_date_input)
else:
    date_range = (start_preset, end_preset)
    st.sidebar.write(f"**Range:** {start_preset} to {end_preset}")

# Convert back to pd.Timestamp for filtering
start_date, end_date = [pd.Timestamp(d) for d in date_range]
mask = (df["date"] >= start_date) & (df["date"] <= end_date)
df_range = df.loc[mask].copy()

# Determine frequency description
time_description = "Monthly" if len(df) < 1000 else "Daily/Monthly"

st.write(f"### Data from {start_date.date()} to {end_date.date()}")
st.write(f"**Total records in selection:** {len(df_range):,}")

if len(df_range) < 2:
    st.warning("Please select a wider date range.")
else:
    # Store the first row for visualization
    first_row = df_range.iloc[0]
    last_row = df_range.iloc[-1]
    
    # Calculate overall performance for the selected period
    st.write("### Overall Performance")
    
    gold_pct = 100 * (last_row["gold"] - first_row["gold"]) / first_row["gold"]
    st.write(f"**Gold:** {gold_pct:+.2f}% change")
    st.write(f"- Start: ${first_row['gold']:.2f} ({first_row['date'].date()})")
    st.write(f"- End: ${last_row['gold']:.2f} ({last_row['date'].date()})")
    
    if pd.notna(first_row.get("sp500")) and pd.notna(last_row.get("sp500")):
        sp500_pct = 100 * (last_row["sp500"] - first_row["sp500"]) / first_row["sp500"]
        st.write(f"**S&P 500:** {sp500_pct:+.2f}% change")
        st.write(f"- Start: {first_row['sp500']:.2f} ({first_row['date'].date()})")
        st.write(f"- End: {last_row['sp500']:.2f} ({last_row['date'].date()})")
        
        if gold_pct > sp500_pct:
            winner = "Gold outperformed"
            diff = gold_pct - sp500_pct
        elif sp500_pct > gold_pct:
            winner = "S&P 500 outperformed"
            diff = sp500_pct - gold_pct
        else:
            winner = "Both performed equally"
            diff = 0
        st.info(f"**{winner}** (Δ {diff:.2f}%)")
    
    st.write("---")
    
    # Visualization section
    st.write("### Price History Visualization")
    
    # Normalize to base 100 at start date for comparison
    df_viz = df_range.copy()
    df_viz['gold_indexed'] = 100 * df_viz['gold'] / first_row['gold']
    
    # Create matplotlib figure for better control
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Add recession shading first (so it's in the background)
    add_recession_shading(ax, start_date, end_date)
    
    # Plot gold
    ax.plot(df_viz['date'], df_viz['gold_indexed'], label='Gold', linewidth=2, color='gold')
    
    if pd.notna(first_row.get("sp500")):
        df_viz['sp500_indexed'] = 100 * df_viz['sp500'] / first_row['sp500']
        # Plot S&P 500
        ax.plot(df_viz['date'], df_viz['sp500_indexed'], label='S&P 500', linewidth=2, color='steelblue')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Indexed Value (Start = 100)', fontsize=12, fontweight='bold')
    ax.set_title('Gold vs S&P 500 Performance (Indexed)', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='best', framealpha=0.9, fontsize=10)
    
    # Add note about recessions
    ax.text(0.02, 0.98, 'Gray areas indicate US recessions', 
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    st.caption("Index: Start of selected period = 100 | Gray shading indicates NBER-defined US recession periods")
    
    # Correlation Analysis Section
    st.write("---")
    st.write("### 📊 Correlation Analysis (PMCC)")
    st.write("**Pearson's Product-Moment Correlation Coefficient** measures the linear relationship between Gold and S&P 500 prices.")
    
    if pd.notna(first_row.get("sp500")) and len(df_range) > 1:
        # Calculate correlation using complete data
        valid_data = df_range[['gold', 'sp500']].dropna()
        
        if len(valid_data) > 1:
            # Calculate Pearson correlation coefficient
            correlation, p_value = stats.pearsonr(valid_data['gold'], valid_data['sp500'])
            
            # Display correlation metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Correlation (r)", f"{correlation:.4f}")
            with col2:
                st.metric("P-value", f"{p_value:.6f}")
            with col3:
                # Interpret correlation strength
                if abs(correlation) >= 0.7:
                    strength = "Strong"
                elif abs(correlation) >= 0.4:
                    strength = "Moderate"
                elif abs(correlation) >= 0.2:
                    strength = "Weak"
                else:
                    strength = "Very Weak"
                
                direction = "Positive" if correlation > 0 else "Negative"
                st.metric("Relationship", f"{strength} {direction}")
            
            # Interpretation guide
            with st.expander("📖 How to interpret correlation"):
                st.write("""
                **Correlation Coefficient (r):**
                - **+1.0**: Perfect positive correlation (both move together)
                - **+0.7 to +1.0**: Strong positive correlation
                - **+0.4 to +0.7**: Moderate positive correlation
                - **+0.2 to +0.4**: Weak positive correlation
                - **-0.2 to +0.2**: Very weak or no correlation
                - **-0.4 to -0.2**: Weak negative correlation
                - **-0.7 to -0.4**: Moderate negative correlation
                - **-1.0 to -0.7**: Strong negative correlation
                - **-1.0**: Perfect negative correlation (move in opposite directions)
                
                **P-value:**
                - **< 0.05**: Statistically significant (relationship likely not due to chance)
                - **≥ 0.05**: Not statistically significant (could be due to random chance)
                
                **Note:** Gold is often considered a "safe haven" asset that may move inversely to equities during market stress,
                but can show positive correlation during bull markets.
                """)
            
            # Scatter plot with trend line
            st.write("#### Scatter Plot: Gold vs S&P 500 with Line of Best Fit")
            
            # Prepare data for scatter plot
            x = valid_data['gold'].values
            y = valid_data['sp500'].values
            
            # Calculate line of best fit using linear regression
            slope, intercept, r_value, p_value_reg, std_err = stats.linregress(x, y)
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Scatter plot
            ax.scatter(x, y, alpha=0.6, s=50, color='steelblue', edgecolors='darkblue', linewidth=0.5, label='Data Points')
            
            # Line of best fit
            x_sorted = np.sort(x)
            line_y = slope * x_sorted + intercept
            ax.plot(x_sorted, line_y, 'r-', linewidth=2, label=f'Best Fit Line (y = {slope:.4f}x + {intercept:.2f})')
            
            # Labels and title
            ax.set_xlabel('Gold Price ($)', fontsize=12, fontweight='bold')
            ax.set_ylabel('S&P 500 Index', fontsize=12, fontweight='bold')
            ax.set_title('Gold vs S&P 500 Price Relationship', fontsize=14, fontweight='bold', pad=20)
            
            # Grid
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Legend
            ax.legend(loc='best', framealpha=0.9)
            
            # Tight layout
            plt.tight_layout()
            
            # Display in Streamlit
            st.pyplot(fig)
            
            # Close figure to free memory
            plt.close(fig)
            
            # Display regression equation and stats
            st.caption(f"**Regression Line:** S&P 500 = {slope:.4f} × Gold + {intercept:.2f}")
            st.caption(f"**Correlation:** r = {correlation:.4f} | Each point represents a date in the selected period")
            
            # Calculate and display coefficient of determination
            r_squared = correlation ** 2
            st.info(f"**R² = {r_squared:.4f}** — {r_squared*100:.2f}% of the variance in one asset can be explained by the other")
            
            # Rolling correlation analysis
            st.write("#### 📈 Rolling Correlation Over Time")
            
            # Add disclaimer about monthly data limitations
            st.markdown("""
            <div style="background-color: #ffcccc; padding: 15px; border-radius: 5px; border-left: 5px solid #ff0000;">
                <strong style="color: #cc0000; font-size: 16px;">⚠️ IMPORTANT LIMITATION:</strong><br>
                <span style="color: #660000;">
                This rolling correlation analysis has <strong>severe limitations</strong> due to monthly data frequency. 
                With only 12 data points per year, even a 12-month window provides minimal statistical reliability. 
                Rolling correlations calculated from monthly data are <strong>highly unstable</strong> and should be 
                interpreted with extreme caution. Daily data would be required for meaningful rolling correlation analysis.
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")  # Add spacing
            
            # Let user select window size
            window_options = {
                "3 months": 3,
                "6 months": 6,
                "12 months": 12,
                "24 months": 24,
                "36 months": 36
            }
            
            window_label = st.selectbox(
                "Rolling window size:",
                list(window_options.keys()),
                index=2  # Default to 12 months
            )
            window_size = window_options[window_label]
            
            if len(valid_data) >= window_size:
                # Calculate rolling correlation
                rolling_corr = valid_data['gold'].rolling(window=window_size).corr(valid_data['sp500'])
                
                # Create rolling correlation chart with matplotlib
                rolling_df = pd.DataFrame({
                    'date': df_range['date'].iloc[:len(rolling_corr)],
                    'Rolling Correlation': rolling_corr.values
                })
                rolling_df = rolling_df.dropna()
                
                # Create matplotlib figure
                fig, ax = plt.subplots(figsize=(12, 5))
                
                # Add recession shading
                add_recession_shading(ax, start_date, end_date)
                
                # Plot rolling correlation
                ax.plot(rolling_df['date'], rolling_df['Rolling Correlation'], 
                       linewidth=2, color='darkgreen', label=f'{window_label} Rolling Correlation')
                
                # Add horizontal line at 0
                ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
                
                # Formatting
                ax.set_xlabel('Date', fontsize=12, fontweight='bold')
                ax.set_ylabel('Correlation Coefficient', fontsize=12, fontweight='bold')
                ax.set_title(f'Rolling {window_label} Correlation: Gold vs S&P 500', 
                            fontsize=14, fontweight='bold', pad=20)
                ax.grid(True, alpha=0.3, linestyle='--')
                ax.legend(loc='best', framealpha=0.9, fontsize=10)
                ax.set_ylim(-1, 1)
                
                # Add note about recessions
                ax.text(0.02, 0.98, 'Gray areas indicate US recessions', 
                       transform=ax.transAxes, fontsize=9, verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
                
                st.caption(f"Rolling {window_label} correlation between Gold and S&P 500 | Gray shading indicates recession periods")
                
                # Summary statistics
                st.write(f"**Rolling Correlation Statistics ({window_label}):**")
                stats_col1, stats_col2, stats_col3 = st.columns(3)
                with stats_col1:
                    st.metric("Mean", f"{rolling_corr.mean():.4f}")
                with stats_col2:
                    st.metric("Min", f"{rolling_corr.min():.4f}")
                with stats_col3:
                    st.metric("Max", f"{rolling_corr.max():.4f}")
            else:
                st.warning(f"Not enough data points for {window_label} rolling correlation. Need at least {window_size} records.")
        else:
            st.warning("Not enough valid data points to calculate correlation.")
    else:
        st.info("S&P 500 data not available for correlation analysis in this period.")

