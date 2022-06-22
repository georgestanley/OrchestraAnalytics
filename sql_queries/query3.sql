--Query3
--Orchestra(s)+continent, within a period of choice; results both in absolute and proportional figures 
select * from continents ;
select * from programs_all where country  not in (select country from continents);

--Part1: Orchestra and Continent wise share
with total as
    ( select Orchestra,sum(counts) as total
    from (select 
    Orchestra,
    Country,
    count(*) counts
from programs_all
where 1=1
group by Orchestra, Country)
group by Orchestra )

select total.Orchestra,continent,total.total, counts,
    round(((counts *1.0) /total.total)*100,2) as share
from (select 
    Orchestra,
    --programs_all.country,
    continents.continent,
    count(*) counts
from programs_all , continents
where 1=1
and programs_all.country = continents.country
group by Orchestra
--, programs_all.Country
,Continent) pageviews,
    total
where pageviews.Orchestra=total.Orchestra
order by total.Orchestra, share desc;


--part2: orchestra as per date-range
with total as
    ( select Orchestra,sum(counts) as total
    from (select 
    Orchestra,
    Country,
    count(*) counts
from programs_all
where 1=1
    and date_of_event  between '1950-01-01' and '1951-01-01' 
group by Orchestra, Country)
group by Orchestra )

select total.Orchestra,Continent,total.total, counts,
    round(((counts *1.0) /total.total)*100,2) as share
from (select 
    Orchestra,
    --Country,
    continents.continent,
    count(*) counts
from programs_all, continents
where 1=1
and programs_all.country = continents.country
and date_of_event  between '1950-01-01' and '1951-01-01' 
group by Orchestra
--, Country
,Continent) pageviews,
    total
where pageviews.Orchestra=total.Orchestra
order by total.Orchestra, share desc;

--part3: Code for creating chart

with total as
    ( select Orchestra,sum(counts) as total
    from (select 
    Orchestra,
    Country,
    count(*) counts
from programs_all
where 1=1
--and Orchestra in ('Vienna Philharmonic')
and date_of_event  between '1950-01-01' and '1960-01-01' 
group by Orchestra, Country)
group by Orchestra )

select Continent, sum(counts) xxx
from  (
select total.Orchestra,Continent,total.total, counts,
    round(((counts *1.0) /total.total)*100,2) as share
from (select 
    Orchestra,
    --Country,
    continents.continent,
    count(*) counts
from programs_all, continents
where 1=1
and programs_all.country = continents.country
and date_of_event  between '1950-01-01' and '1951-01-01' 
group by Orchestra
--, Country
,Continent) pageviews,
    total
where pageviews.Orchestra=total.Orchestra
order by total.Orchestra, share desc) 
group by Continent
order by xxx desc;

--Query4 : as per selected orchestra for given time range
with total as
    ( select Orchestra,sum(counts) as total
    from (select 
    Orchestra,
    Country,
    count(*) counts
from programs_all
where 1=1
and Orchestra in 
("Bamberg Symphony","Berlin Philharmonic")    
and date_of_event  between '1950-01-01' and '1960-01-01' 
group by Orchestra, Country)
group by Orchestra )

select total.Orchestra,Continent,total.total, counts,
    round(((counts *1.0) /total.total)*100,2) as share
from (select 
    Orchestra,
    --Country,
    Continents.continent,
    count(*) counts
from programs_all, continents
where 1=1
and programs_all.country = continents.country
and date_of_event  between '1950-01-01' and '1960-01-01' 
group by Orchestra, Continent) pageviews,
    total
where pageviews.Orchestra=total.Orchestra
order by total.Orchestra, share desc;

--Query : Orchestra choice-wise chart
with total as
    ( select Orchestra,sum(counts) as total
    from (select 
    Orchestra,
    Country,
    count(*) counts
from programs_all
where 1=1
--and Orchestra in ('Vienna Philharmonic')
    and date_of_event  between '1950-01-01' and '1961-01-01' 
group by Orchestra, Country)
group by Orchestra )

select continent,sum(counts) xxx
from (
select total.Orchestra,Continent,total.total, counts,
    round(((counts *1.0) /total.total)*100,2) as share
from (select 
    Orchestra,
    --Country,
    continents.continent,
    count(*) counts
from programs_all , continents
where 1=1
and programs_all.country=continents.country
    and date_of_event  between '1950-01-01' and '1960-01-01' 
group by Orchestra, continent) pageviews,
    total
where pageviews.Orchestra=total.Orchestra
and total.Orchestra in 
("Bamberg Symphony","Berlin Philharmonic")
order by total.Orchestra, share desc)
group by continent;

--dsiplaying compltee data continent wise

select pa.event_id, pa.date_of_event,co.continent, pa.country, pa.place, pa.Orchestra,group_concat(pl.program) program, group_concat(distinct c.conductor) conductor
 from programs_all pa, program_list pl ,conductors c, continents co
where 1=1
and pa.event_id=pl.event_id
and pa.event_id=c.event_id
and pa.country= co.country
and co.continent = 'Africa'
group by pa.event_id, pa.date_of_event,co.continent, pa.country, pa.place, pa.Orchestra;


