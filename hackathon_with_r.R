phy_comp_db <- readRDS('~/Downloads/phy_comp_db.rds')
phy_comp_db <- sqldf('select * from phy_comp_db')
phy_comp_db$Zip_Code <- pa("%05s", phy_comp_db$Zip_Code)
geocoding <- read.csv('~/Downloads/zip_codes_states.csv', colClasses=c(zip_code="character"))
library('sqldf')
#phy_comp_db <- sqldf('select * from phy_comp_db')
#phy_comp_db <- sqldf('select * , 
#                      CASE WHEN LENGTH(Zip_Code) = 4 THEN "0" || Zip_Code else Zip_Code END as zip_fix
#                      from phy_comp_db')

distinct_npi <- sqldf('select DISTINCT NPI
                      from phy_comp_db')

clinic_size <- sqldf('select DISTINCT Organization_legal_name as org, 
                      SUBSTR(cast(Zip_Code as text), 1, 5) as zc, 
                      count(SUBSTR(cast(Zip_Code as text), 1, 5)) as c_zc, count(DISTINCT NPI) as docs
                      from phy_comp_db
                      WHERE Primary_specialty LIKE "%onco%" OR 
                            Primary_specialty like "%hema%" OR 
                            Primary_specialty like "%radi%" 
                      group by org
                      order by count(DISTINCT NPI) DESC')

common_zc <- sqldf('select org, MAX(c_zc || "." || SUBSTR(zc, 1)) as combin_zc, MAX(docs) as doc_max
                    from clinic_size
                    group by org
                    order by MAX(docs) DESC')

split_zc <- sqldf('select org, doc_max, 
                   SUBSTR(combin_zc, charindex(".", combin_zc)+1, LENGTH(combin_zc)-1) as zip_code,
                   SUBSTR(combin_zc, 1, charindex(".", combin_zc)-1) as count_zip_code
                   from common_zc')

#fix_leading_zero <- sqldf('select org, doc_max,
#                           CASE WHEN LENGTH(zip_code) = 4 THEN "0" || zip_code else zip_code END as zip_code,
#                           count_zip_code
#                           from split_zc WHERE doc_max >= 100')

distinct_specialties <- sqldf('select distinct Primary_specialty, 
                               count(DISTINCT NPI) as count
                               from phy_comp_db
                               WHERE Primary_specialty 
                               LIKE "%onco%" OR 
                               Primary_specialty like "%hema%" OR 
                               Primary_specialty like "%radi%"
                               GROUP BY Primary_specialty
                               ORDER BY count DESC')

zc_to_geocode <- sqldf('select split_zc.org, cast(split_zc.doc_max as text) as docs, split_zc.zip_code, split_zc.count_zip_code, geocoding.latitude as latitude, geocoding.longitude as longitude 
                        from split_zc
                        LEFT OUTER JOIN geocoding
                        ON geocoding.zip_code = split_zc.zip_code
                        ORDER BY split_zc.org')

write.csv(file='~/Desktp/cancer_center_locations.csv', x=zc_to_geocode)