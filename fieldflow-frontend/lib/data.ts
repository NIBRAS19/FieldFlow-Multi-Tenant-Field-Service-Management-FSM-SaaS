export const nav = [
  ['dashboard','Dashboard'],['requests','Requests'],['work-orders','Work Orders'],['schedule','Schedule'],['dispatch','Dispatch'],['customers','Customers'],['technicians','Technicians'],['assets','Assets'],['invoices','Invoices'],['reports','Reports']
] as const;

export const jobs = [
  {id:'WO-1045',customer:'ABC Trading LLC',location:'Office Building A',tech:'Ahmed Hassan',service:'AC Maintenance',priority:'High',status:'On Site',time:'10:00–12:00',sla:'02h 18m'},
  {id:'WO-1046',customer:'Nexa Facilities',location:'Warehouse 3',tech:'Sara Ali',service:'Electrical Inspection',priority:'Medium',status:'In Progress',time:'11:30–13:00',sla:'01h 06m'},
  {id:'WO-1047',customer:'Greenline Cafe',location:'Al Khalidiyah',tech:'Omar Khan',service:'Plumbing Repair',priority:'Urgent',status:'En Route',time:'12:00–13:00',sla:'00h 44m'},
  {id:'WO-1048',customer:'Vertex Clinic',location:'Muroor Branch',tech:'Unassigned',service:'HVAC Service',priority:'High',status:'Unassigned',time:'14:00–15:30',sla:'03h 10m'},
  {id:'WO-1049',customer:'Nova Retail',location:'Reem Mall',tech:'Ahmed Hassan',service:'Equipment Check',priority:'Low',status:'Scheduled',time:'15:00–16:00',sla:'04h 45m'},
];

export const technicians = [
  {name:'Ahmed Hassan',initials:'AH',status:'En Route',jobs:5,completed:3,util:86,area:'Abu Dhabi'},
  {name:'Sara Ali',initials:'SA',status:'On Site',jobs:4,completed:2,util:74,area:'Mussafah'},
  {name:'Omar Khan',initials:'OK',status:'Available',jobs:3,completed:3,util:63,area:'Khalifa City'},
  {name:'Lina Joseph',initials:'LJ',status:'Offline',jobs:2,completed:1,util:41,area:'Al Ain'},
];

export const customers = [
  {name:'ABC Trading LLC',contact:'Mariam Rahman',phone:'+971 50 123 4456',locations:3,jobs:12,balance:'AED 4,280',status:'Active'},
  {name:'Nexa Facilities',contact:'Faisal Noor',phone:'+971 55 334 1182',locations:5,jobs:28,balance:'AED 9,840',status:'Active'},
  {name:'Greenline Cafe',contact:'Aisha Ali',phone:'+971 52 764 2201',locations:2,jobs:8,balance:'AED 0',status:'Active'},
  {name:'Vertex Clinic',contact:'Omar Saeed',phone:'+971 56 210 6789',locations:1,jobs:4,balance:'AED 1,120',status:'Active'},
  {name:'Nova Retail',contact:'Ryan George',phone:'+971 50 340 1143',locations:4,jobs:18,balance:'AED 2,410',status:'Active'},
];

export const requests = [
  {id:'REQ-1093',customer:'Vertex Clinic',issue:'AC not cooling',priority:'High',status:'New',created:'Today, 09:42'},
  {id:'REQ-1092',customer:'Greenline Cafe',issue:'Sink leaking under counter',priority:'Urgent',status:'Approved',created:'Today, 08:55'},
  {id:'REQ-1091',customer:'ABC Trading LLC',issue:'Quarterly AC maintenance',priority:'Medium',status:'Converted',created:'Yesterday, 16:20'},
  {id:'REQ-1090',customer:'Nova Retail',issue:'Freezer temperature alarm',priority:'High',status:'In Review',created:'Yesterday, 13:15'},
];

export const invoices = [
  {id:'INV-2026-0092',customer:'ABC Trading LLC',amount:'AED 1,890',due:'18 Sep 2026',status:'Paid'},
  {id:'INV-2026-0091',customer:'Nexa Facilities',amount:'AED 4,860',due:'22 Sep 2026',status:'Sent'},
  {id:'INV-2026-0090',customer:'Vertex Clinic',amount:'AED 1,120',due:'12 Sep 2026',status:'Overdue'},
  {id:'INV-2026-0089',customer:'Nova Retail',amount:'AED 2,410',due:'25 Sep 2026',status:'Draft'},
];
