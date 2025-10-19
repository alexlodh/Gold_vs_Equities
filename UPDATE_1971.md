# 1971-Present Analysis Update

## What Changed

The application has been updated to focus on the **most meaningful period** for Gold vs S&P 500 comparison:

### 📅 **Date Range: 1971 - Present**

**Why 1971?**
- August 15, 1971: President Nixon ended the gold standard
- This marks the beginning of "fiat currency" era
- Both assets became truly comparable investments
- Most relevant for modern portfolio analysis

### 📊 **Enhanced Data**

- **658 monthly records** from January 1971 to October 2025
- **Historical Gold Prices**: From histprices.json (monthly data)
- **S&P 500 Index**: Fetched from Yahoo Finance API (complete history)
- **Both assets** have complete data for the entire period

### 🎯 **Key Features**

1. **Complete Historical Coverage**
   - Full 54+ years of both gold and S&P 500 data
   - No gaps or missing data
   - Monthly frequency for clean long-term analysis

2. **Updated Preset Ranges**
   - Last 1, 5, 10, 20 years
   - Since 2000 (21st century)
   - Since 1980 (modern era)
   - Since 1971 (complete dataset)

3. **Optimized Analysis**
   - Focused on relevant investment period
   - Cleaner data with fewer anomalies
   - More meaningful comparisons

### 🔄 **Data Generation**

To regenerate the dataset:
```bash
python src/preprocess_1971.py
```

This will:
1. Load historical gold prices from histprices.json (1971+)
2. Fetch S&P 500 data from Yahoo Finance (1971+)
3. Create monthly resampled, aligned dataset
4. Save to `data/gold_sp500_aligned.csv`

### 📈 **Analysis Periods**

Now focuses on economically significant eras:
- **1971-1980**: Post-gold standard adjustment
- **1980-2000**: Modern bull market
- **2000-2008**: Dot-com crash and recovery
- **2008-2020**: Financial crisis and recovery
- **2020-Present**: COVID-19 and beyond

### 🎊 **Results**

- **Dataset**: 658 records (monthly)
- **Gold Range**: $37.88 (1971) to $3,352.66 (2025)
- **S&P 500 Range**: 63.54 (1971) to 6,688.46 (2025)
- **Time Span**: 54 years, 9 months

This provides the most relevant and complete dataset for comparing gold and equity performance in the modern investment era.
