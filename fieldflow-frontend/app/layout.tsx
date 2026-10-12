import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'FieldFlow — Field Service Operations SaaS',
  description: 'A production-style frontend for field service teams.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
