export function formatDateTime(value: string | null | undefined): string {
  if (!value) return "—";
  return new Date(value).toLocaleString();
}

export function timeUntil(value: string | null | undefined): string {
  if (!value) return "—";
  const diffMs = new Date(value).getTime() - Date.now();
  const overdue = diffMs < 0;
  const abs = Math.abs(diffMs);
  const hours = Math.floor(abs / (1000 * 60 * 60));
  const minutes = Math.floor((abs % (1000 * 60 * 60)) / (1000 * 60));
  const label = hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;
  return overdue ? `Overdue by ${label}` : `${label} remaining`;
}

export const CATEGORIES = [
  "Pothole", "Road Damage", "Garbage", "Broken Streetlight",
  "Water Leakage", "Drainage", "Fallen Tree", "Damaged Road Sign", "General Civic Issue",
];
