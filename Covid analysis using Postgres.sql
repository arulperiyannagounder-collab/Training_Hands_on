drop table covid;
create table covid (
Country_Region varchar(50) not null ,
Confirmed int not null ,
Deaths int not null ,
Recovered int not null ,
Active int not null ,
New_cases int not null ,       
New_deaths int not null ,
New_recovered int not null ,
Deaths_per_100_Cases numeric not null ,
Recovered_per_100_Cases numeric not null ,
Deaths_per_100_Recovered numeric not null ,
Confirmed_last_week int not null ,
one_week_change int not null ,
one_week_increase numeric not null ,
WHO_Region varchar(50) not null 



);
select Confirmed,Deaths,Recovered from covid;

select Country_Region from covid where WHO_Region='Europe';


select Country_Region from covid where Confirmed>1000;


select Country_Region, Active from covid order by Active desc ;


select count (Country_Region) from covid;

select Country_Region from covid order by Deaths  desc limit 5 ;


select Country_Region from covid where Recovered> Active;


select Country_Region from covid where Deaths_per_100_Recovered > (select avg(Deaths_per_100_Recovered) from covid  );

select Country_Region from covid where Confirmed-Confirmed_last_week > 25%Confirmed_last_week;

select Country_Region from (select max( Confirmed) from covid)   ;