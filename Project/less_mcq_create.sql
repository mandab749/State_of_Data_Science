CREATE TABLE less_mcq as (
  SELECT survey_time as survey_time,
         q1 as Age,
         q2 as Gender,
         q3 as Country,
         q10 as yearly_compensation,
         q11 as spending_on_cloud,
         q15 as experience_coding,
         q19 as recommended_language,
         q23 as machine_learning_experience,
         q22 as tpu_usage
  FROM mcq
) ;



 -- ('India', 'United States of America', 'Brazil', 'Japan', 'Russia', 'China', 'Germany', 'United Kingdom of Great Britain and Northern Ireland', 'Canada', 'Spain')
