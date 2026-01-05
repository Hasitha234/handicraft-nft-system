import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Design System | LAKARCADE",
  description: "AI-Assisted Design Recommendation System for Sri Lankan Handicrafts",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-neutiva antialiased">
        {children}
      </body>
    </html>
  );
}
