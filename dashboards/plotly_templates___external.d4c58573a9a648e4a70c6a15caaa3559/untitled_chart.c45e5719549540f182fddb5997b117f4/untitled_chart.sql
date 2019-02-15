select
  'Debug' as stage, 20 as val, 75 as current_val
union all select 'Info', 40, 75
union all select 'Warn', 60, 75
union all select 'Error', 80, 75
union all select 'Fatal', 100, 75