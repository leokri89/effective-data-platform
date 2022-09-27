--For example, if we care about high or low values that occur only 5% of the time by random chance, we’d use a z score threshold of +/- 1.645. If we want a 5% threshold exclusively for high values, we’d pick 1.96.

-- ABS: Two-tailed test, exemplo: abs(zscore) >= 1.645 
-- Two-tailed 5% of the time by random chance: abs(zscore) >= 1.645
-- % threshold exclusively for high values: zscore >= 1.96
-- % threshold exclusively for low values: zscore <= -1.96

with data as (
    select
        date_trunc('day', created_at)::date as day,
        count(1) as value
    from disk_usage
    group by 1
), data_with_stddev as (
    select
        day,
        value,
        (value - avg(value) over ()) / (stddev(value) over ()) as zscore
    from data
    order by 1
)
select 
    day,
    value,
    zscore,
    case
        when abs(zscore) >= 1.645 then "Outlier"
        else "Normal"
    end test_result
from data_with_stddev