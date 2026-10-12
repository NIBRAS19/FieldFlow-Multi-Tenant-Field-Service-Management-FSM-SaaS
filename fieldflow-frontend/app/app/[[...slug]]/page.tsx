import {AppRouter} from '@/components/fieldflow';

export default async function Page({params}:{params:Promise<{slug?:string[]}>}){
  const p=await params;
  const page=p.slug?.[0]||'dashboard';
  return <AppRouter page={page}/>;
}
