import { loadDashboardDataset } from "@/lib/data";
import { Dashboard } from "@/components/dashboard";

export default async function Page() {
  const dataset = await loadDashboardDataset();
  return <Dashboard {...dataset} />;
}
