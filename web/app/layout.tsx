import type { Metadata } from "next";
import "./globals.css";
import { cn } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Gold vs S&P 500 Dashboard",
  description: "Shadcn-based dashboard comparing gold and S&P 500 performance since 1971."
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn("bg-background text-foreground font-sans")}>
        {children}
      </body>
    </html>
  );
}
