"use client";

import { useMemo, useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import {
  differenceInCalendarMonths,
  format,
  isAfter,
  isBefore,
  parseISO,
  subYears
} from "date-fns";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  ScatterChart,
  Scatter,
  Line,
  ReferenceArea
} from "recharts";
import { CalendarIcon, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import type { DashboardDataset } from "@/lib/data";
import {
  buildNormalizedSeries,
  calculateCorrelationSummary,
  calculatePerformance,
  calculateRollingCorrelation,
  filterDataByRange
} from "@/lib/analytics";
import { RECESSION_PERIODS } from "@/lib/constants";
import { cn } from "@/lib/utils";

const PRESET_OPTIONS = [
  { label: "Custom", value: "custom" },
  { label: "Last 1 Year", value: "1y" },
  { label: "Last 5 Years", value: "5y" },
  { label: "Last 10 Years", value: "10y" },
  { label: "Last 20 Years", value: "20y" },
  { label: "Since 2000", value: "2000" },
  { label: "Since 1980", value: "1980" },
  { label: "Since 1971 (All Data)", value: "all" }
];

const ROLLING_WINDOWS = [
  { label: "3 months", value: 3 },
  { label: "6 months", value: 6 },
  { label: "12 months", value: 12 },
  { label: "24 months", value: 24 },
  { label: "36 months", value: 36 }
];

interface DashboardProps extends DashboardDataset {}

function clampDate(date: Date, min: Date, max: Date) {
  if (isBefore(date, min)) return min;
  if (isAfter(date, max)) return max;
  return date;
}

function applyPreset(
  preset: string,
  minDate: Date,
  maxDate: Date
): { from: Date; to: Date } {
  switch (preset) {
    case "1y":
      return { from: clampDate(subYears(maxDate, 1), minDate, maxDate), to: maxDate };
    case "5y":
      return { from: clampDate(subYears(maxDate, 5), minDate, maxDate), to: maxDate };
    case "10y":
      return { from: clampDate(subYears(maxDate, 10), minDate, maxDate), to: maxDate };
    case "20y":
      return { from: clampDate(subYears(maxDate, 20), minDate, maxDate), to: maxDate };
    case "2000":
      return {
        from: clampDate(new Date(2000, 0, 1), minDate, maxDate),
        to: maxDate
      };
    case "1980":
      return {
        from: clampDate(new Date(1980, 0, 1), minDate, maxDate),
        to: maxDate
      };
    case "all":
      return { from: minDate, to: maxDate };
    case "custom":
    default:
      return { from: minDate, to: maxDate };
  }
}

export function Dashboard({ data, info }: DashboardProps) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();

  const minDate = useMemo(() => parseISO(info.minDate), [info.minDate]);
  const maxDate = useMemo(() => parseISO(info.maxDate), [info.maxDate]);

  const [preset, setPreset] = useState<string>("all");
  const [range, setRange] = useState<{ from: Date; to: Date }>({
    from: minDate,
    to: maxDate
  });

  const [rollingWindow, setRollingWindow] = useState<number>(12);

  const handlePresetChange = (value: string) => {
    setPreset(value);
    if (value !== "custom") {
      const nextRange = applyPreset(value, minDate, maxDate);
      setRange(nextRange);
    }
  };

  const handleRangeChange = (next?: { from?: Date; to?: Date }) => {
    if (!next?.from || !next?.to) return;
    const nextFrom = new Date(next.from);
    const nextTo = new Date(next.to);
    setRange({
      from: clampDate(nextFrom, minDate, maxDate),
      to: clampDate(nextTo, minDate, maxDate)
    });
  };

  const filtered = useMemo(() => {
    const sorted = [...data].sort(
      (a, b) => parseISO(a.date).getTime() - parseISO(b.date).getTime()
    );
    return filterDataByRange(sorted, range.from, range.to);
  }, [data, range.from, range.to]);

  const performance = useMemo(() => {
    if (filtered.length < 2) return null;
    return calculatePerformance(filtered);
  }, [filtered]);

  const normalized = useMemo(() => buildNormalizedSeries(filtered), [filtered]);
  const correlation = useMemo(
    () => (filtered.length > 2 ? calculateCorrelationSummary(filtered) : null),
    [filtered]
  );

  const scatterData = useMemo(
    () =>
      filtered
        .filter((d) => !Number.isNaN(d.gold) && !Number.isNaN(d.sp500))
        .map((d) => ({
          gold: d.gold,
          sp500: d.sp500
        })),
    [filtered]
  );

  const rolling = useMemo(
    () => calculateRollingCorrelation(filtered, rollingWindow),
    [filtered, rollingWindow]
  );

  const frequency =
    differenceInCalendarMonths(maxDate, minDate) > data.length / 2
      ? "Monthly"
      : "Daily";

  const refreshData = () => {
    startTransition(() => {
      router.refresh();
    });
  };

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="border-b border-border">
        <div className="mx-auto flex w-full max-w-6xl flex-col gap-2 px-6 py-6">
          <p className="text-sm uppercase text-muted-foreground">
            Gold vs S&P 500
          </p>
          <h1 className="text-3xl font-bold">
            Historical Comparison (1971 - Present)
          </h1>
          <p className="text-muted-foreground">
            Compare gold and S&P 500 performance since 1971 – the year the US left the
            gold standard.
          </p>
        </div>
      </header>

      <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-6 px-6 py-6 lg:flex-row">
        <aside className="w-full shrink-0 space-y-4 lg:w-80">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span role="img" aria-label="chart">
                  📊
                </span>
                Analysis Settings
              </CardTitle>
              <CardDescription>
                Note: Pre-2000 gold data may remain monthly due to historical data
                availability.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button
                className="w-full"
                onClick={refreshData}
                disabled={isPending}
              >
                {isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Refreshing…
                  </>
                ) : (
                  "Refresh data"
                )}
              </Button>
              <Separator />
              <div className="space-y-1 text-sm">
                <p>
                  <span className="font-semibold">Data file used:</span>{" "}
                  {info.fileName}
                </p>
                <p>
                  <span className="font-semibold">Data file modified:</span>{" "}
                  {format(parseISO(info.modified), "yyyy-MM-dd HH:mm:ss")}
                </p>
                <p>
                  <span className="font-semibold">Data Range:</span>{" "}
                  {format(minDate, "yyyy-MM-dd")} – {format(maxDate, "yyyy-MM-dd")}
                </p>
                <p>
                  <span className="font-semibold">Total Records:</span>{" "}
                  {info.total.toLocaleString()}
                </p>
                <p>
                  <span className="font-semibold">Frequency:</span> {frequency}
                </p>
              </div>
              <Separator />
              <div className="space-y-3">
                <div className="space-y-2">
                  <Label htmlFor="preset">Preset Ranges</Label>
                  <Select value={preset} onValueChange={handlePresetChange}>
                    <SelectTrigger id="preset">
                      <SelectValue placeholder="Select range" />
                    </SelectTrigger>
                    <SelectContent>
                      {PRESET_OPTIONS.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Date Range</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        className={cn(
                          "w-full justify-start text-left font-normal",
                          !range && "text-muted-foreground"
                        )}
                      >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {range.from && range.to ? (
                          <>
                            {format(range.from, "MMM d, yyyy")} -{" "}
                            {format(range.to, "MMM d, yyyy")}
                          </>
                        ) : (
                          <span>Select date range</span>
                        )}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar
                        initialFocus
                        mode="range"
                        numberOfMonths={2}
                        selected={{
                          from: range.from,
                          to: range.to
                        }}
                        defaultMonth={range.from}
                        onSelect={(selectedRange) => {
                          setPreset("custom");
                          handleRangeChange(selectedRange);
                        }}
                        disabled={(date) =>
                          isBefore(date, minDate) || isAfter(date, maxDate)
                        }
                      />
                    </PopoverContent>
                  </Popover>
                </div>
              </div>
            </CardContent>
          </Card>
        </aside>

        <section className="flex-1 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>
                Data from {format(range.from, "yyyy-MM-dd")} to{" "}
                {format(range.to, "yyyy-MM-dd")}
              </CardTitle>
              <CardDescription>
                {filtered.length.toLocaleString()} records in selection
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {performance ? (
                <div className="grid gap-4 md:grid-cols-2">
                  <Card className="border-primary/40 bg-primary/5">
                    <CardHeader>
                      <CardTitle>Gold</CardTitle>
                      <CardDescription>
                        {format(parseISO(filtered[0].date), "yyyy-MM-dd")} to{" "}
                        {format(parseISO(filtered[filtered.length - 1].date), "yyyy-MM-dd")}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-1">
                      <p className="text-3xl font-semibold">
                        {performance.goldPct >= 0 ? "+" : ""}
                        {performance.goldPct.toFixed(2)}%
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Start: ${performance.goldStart.toFixed(2)}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        End: ${performance.goldEnd.toFixed(2)}
                      </p>
                    </CardContent>
                  </Card>

                  {performance.sp500Pct !== undefined && (
                    <Card className="border-muted/40 bg-muted/10">
                      <CardHeader>
                        <CardTitle>S&amp;P 500</CardTitle>
                        <CardDescription>
                          {format(parseISO(filtered[0].date), "yyyy-MM-dd")} to{" "}
                          {format(parseISO(filtered[filtered.length - 1].date), "yyyy-MM-dd")}
                        </CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-1">
                        <p className="text-3xl font-semibold">
                          {performance.sp500Pct! >= 0 ? "+" : ""}
                          {performance.sp500Pct!.toFixed(2)}%
                        </p>
                        <p className="text-sm text-muted-foreground">
                          Start: {performance.sp500Start?.toFixed(2)}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          End: {performance.sp500End?.toFixed(2)}
                        </p>
                      </CardContent>
                    </Card>
                  )}
                </div>
              ) : (
                <p className="text-muted-foreground">
                  Select a wider date range to view performance metrics.
                </p>
              )}

              {performance && (
                <div className="rounded-lg border border-border bg-muted/20 p-4">
                  <p className="font-semibold">{performance.winner}</p>
                  <p className="text-sm text-muted-foreground">
                    Δ {performance.diff.toFixed(2)}%
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Price History (Indexed)</CardTitle>
              <CardDescription>
                Start of selected period = 100. Gray shading indicates NBER-defined US
                recessions.
              </CardDescription>
            </CardHeader>
            <CardContent className="h-[360px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={normalized} margin={{ top: 20, right: 20, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" opacity={0.4} />
                  <XAxis
                    dataKey="date"
                    tickFormatter={(value) => format(parseISO(value), "yyyy")}
                    stroke="hsl(var(--muted-foreground))"
                  />
                  <YAxis
                    stroke="hsl(var(--muted-foreground))"
                    tickFormatter={(value) => value.toFixed(0)}
                  />
                  <Tooltip
                    contentStyle={{
                      background: "hsl(var(--background))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "0.5rem"
                    }}
                    labelFormatter={(label) =>
                      format(parseISO(label as string), "yyyy-MM-dd")
                    }
                  />
                  <Legend />
                  {RECESSION_PERIODS.map((period) => (
                    <ReferenceArea
                      key={period.start}
                      x1={period.start}
                      x2={period.end}
                      fill="hsl(var(--muted))"
                      fillOpacity={0.25}
                    />
                  ))}
                  <Area
                    type="monotone"
                    dataKey="goldIndex"
                    name="Gold"
                    stroke="#facc15"
                    fill="#facc15"
                    fillOpacity={0.2}
                    strokeWidth={2}
                    dot={false}
                  />
                  <Area
                    type="monotone"
                    dataKey="sp500Index"
                    name="S&P 500"
                    stroke="#60a5fa"
                    fill="#60a5fa"
                    fillOpacity={0.15}
                    strokeWidth={2}
                    dot={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {correlation && (
            <Card>
              <CardHeader>
                <CardTitle>Correlation Analysis (PMCC)</CardTitle>
                <CardDescription>
                  Pearson correlation between Gold and S&amp;P 500 for the selected range.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid gap-4 md:grid-cols-4">
                  <Metric label="Correlation (r)" value={correlation.correlation} format="number" />
                  <Metric label="P-value" value={correlation.pValue} format="pvalue" />
                  <Metric
                    label="Relationship"
                    value={correlation.direction === "Neutral"
                      ? correlation.direction
                      : `${correlation.strength} ${correlation.direction}`}
                    format="string"
                  />
                  <Metric label="R²" value={correlation.rSquared} format="percent" />
                </div>

                <details className="rounded-lg border border-border bg-card/40 p-4">
                  <summary className="cursor-pointer font-semibold">
                    How to interpret correlation
                  </summary>
                  <div className="mt-2 space-y-2 text-sm text-muted-foreground">
                    <p>Correlation coefficient ranges from -1 (perfect negative) to +1 (perfect positive).</p>
                    <p>P-values under 0.05 suggest the relationship is statistically significant.</p>
                    <p>
                      Gold often acts as a safe haven. Negative correlations may appear during market stress even if long-term correlation is positive.
                    </p>
                  </div>
                </details>

                <div className="h-[320px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart>
                      <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" opacity={0.4} />
                      <XAxis
                        dataKey="gold"
                        type="number"
                        stroke="hsl(var(--muted-foreground))"
                        name="Gold ($)"
                      />
                      <YAxis
                        dataKey="sp500"
                        type="number"
                        stroke="hsl(var(--muted-foreground))"
                        name="S&P 500"
                      />
                      <Tooltip
                        cursor={{ strokeDasharray: "3 3" }}
                        contentStyle={{
                          background: "hsl(var(--background))",
                          border: "1px solid hsl(var(--border))",
                          borderRadius: "0.5rem"
                        }}
                        formatter={(value: number, name: string) => [
                          value.toFixed(2),
                          name
                        ]}
                      />
                      <Scatter data={scatterData} fill="#60a5fa" name="Data points" />
                      <Line
                        type="linear"
                        dataKey={(d: any) =>
                          correlation.slope * d.gold + correlation.intercept
                        }
                        data={scatterData}
                        stroke="#f97316"
                        name="Best fit line"
                        dot={false}
                      />
                    </ScatterChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-sm text-muted-foreground">
                  Regression Line: S&amp;P 500 = {correlation.slope.toFixed(4)} × Gold +
                  {" "}{correlation.intercept.toFixed(2)}
                </p>
              </CardContent>
            </Card>
          )}

          <Card>
            <CardHeader>
              <CardTitle>Rolling Correlation</CardTitle>
              <CardDescription>
                Interpret with caution: monthly data produces unstable rolling correlations.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="rounded-lg border border-destructive/40 bg-destructive/10 p-4 text-sm text-destructive-foreground">
                <p className="font-semibold">Important Limitation</p>
                <p>
                  Rolling correlations over monthly data provide limited statistical reliability.
                  Daily data would yield more trustworthy insights.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <Label htmlFor="rolling-window">Window size</Label>
                <Select
                  value={String(rollingWindow)}
                  onValueChange={(value) => setRollingWindow(Number(value))}
                >
                  <SelectTrigger id="rolling-window" className="w-40">
                    <SelectValue placeholder="Window" />
                  </SelectTrigger>
                  <SelectContent>
                    {ROLLING_WINDOWS.map((option) => (
                      <SelectItem key={option.value} value={String(option.value)}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={rolling}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" opacity={0.4} />
                    <XAxis
                      dataKey="date"
                      stroke="hsl(var(--muted-foreground))"
                      tickFormatter={(value) => format(parseISO(value), "yyyy")}
                    />
                    <YAxis
                      domain={[-1, 1]}
                      stroke="hsl(var(--muted-foreground))"
                      tickFormatter={(value) => value.toFixed(1)}
                    />
                    <Tooltip
                      contentStyle={{
                        background: "hsl(var(--background))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "0.5rem"
                      }}
                      labelFormatter={(label) =>
                        format(parseISO(label as string), "yyyy-MM-dd")
                      }
                    />
                    <Area
                      type="monotone"
                      dataKey="value"
                      stroke="#34d399"
                      fill="#34d399"
                      fillOpacity={0.2}
                      name="Rolling correlation"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </section>
      </main>
    </div>
  );
}

interface MetricProps {
  label: string;
  value: number | string;
  format: "number" | "pvalue" | "percent" | "string";
}

function Metric({ label, value, format }: MetricProps) {
  let display = value;
  if (typeof value === "number") {
    switch (format) {
      case "number":
        display = value.toFixed(4);
        break;
      case "pvalue":
        display = value < 0.0001 ? "< 0.0001" : value.toFixed(4);
        break;
      case "percent":
        display = `${(value * 100).toFixed(2)}%`;
        break;
      default:
        display = value.toString();
    }
  }
  return (
    <div className="rounded-lg border border-border bg-card/60 p-3">
      <p className="text-xs uppercase text-muted-foreground">{label}</p>
      <p className="text-xl font-semibold">{display}</p>
    </div>
  );
}
