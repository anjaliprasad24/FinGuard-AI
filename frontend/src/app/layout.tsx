import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "AI Finance Controller",
  description: "Autonomous AI Finance Controller & Copilot with XAI Anomaly Engine",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">{children}</main>
      </body>
    </html>
  );
}
