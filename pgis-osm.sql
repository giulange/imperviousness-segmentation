-- DROP TABLE public.buildings

SELECT *
	FROM public.buildings
	LIMIT 10

-- may contain duplicates
SELECT COUNT(*)
	FROM public.buildings
	
-- try count without duplicates

	

SELECT ST_NumGeometries(geometry)
	FROM public.buildings
	
SELECT SUM(ST_NumGeometries(geometry))
	FROM public.buildings




SELECT *
	FROM public.buildings a
	WHERE ST_Intersects( a.geometry, 
						ST_GeomFromText('
							POLYGON((13.8 41.5, 13.9 41.5, 13.9 41.0, 13.8 41.0, 13.8 41.5))
										',4326))


SELECT ST_GeometryType(a.geometry),*
	FROM public.buildings a
	WHERE ST_Intersects( ST_Transform(a.geometry,32633), 
						ST_GeomFromText('
							POLYGON ((399960 4600020, 410060 4600020, 410060 4563920, 399960 4563920, 399960 4600020))
										',32633))



SELECT ST_GeometryType(a.geometry),*
	FROM public.buildings a
	WHERE ST_Intersects( ST_Transform(a.geometry,32633), 
						ST_GeomFromText('
							POLYGON ((399960 4600020, 410060 4600020, 410060 4563920, 399960 4563920, 399960 4600020))
										',32633))


SELECT ST_GeometryType(a.geometry),ST_Transform(a.geometry,32633)
	FROM public.buildings a
	WHERE ST_Intersects( ST_Transform(a.geometry,32633), 
						ST_GeomFromText('
							POLYGON ((399960 4600020, 410060 4600020, 410060 4563920, 399960 4563920, 399960 4600020))
										',32633))


SELECT *
	FROM public.buildings a
	WHERE ST_Intersects( ST_Transform(a.geometry,32633), 
						 ST_GeomFromText('
							POLYGON((503660.0 4496320.0, 509760.0 4496320.0, 509760.0 4490220.0, 503660.0 4490220.0, 503660.0 4496320.0))'
							,32633))

--*** Check that ST_Intersects actually clip geometries within defined "POLYGON" ***
-- right-top:    40.607530, 15.057539
-- right-bottom: 40.604757, 15.057517
-- left-bottom:  40.605697, 15.054347
-- left-top:     40.607542, 15.054331

SELECT ST_Intersection(a.geometry, b.geometry)
	FROM public.buildings a JOIN ST_GeomFromText('POLYGON((15.057539 40.607530, 15.057517 40.604757, 15.054347 40.605697, 15.054331 40.607542, 15.057539 40.607530))',4326) as b
	ON ST_Intersects(a.geometry, b.geometry)

-- using :: POLYGON((503660.0 4496320.0, 509760.0 4496320.0, 509760.0 4490220.0, 503660.0 4490220.0, 503660.0 4496320.0))
SELECT ST_Intersection(ST_Transform(a.geometry,32633), b.geometry),*
	FROM public.buildings a JOIN ST_GeomFromText('POLYGON((503660.0 4496320.0, 509760.0 4496320.0, 509760.0 4490220.0, 503660.0 4490220.0, 503660.0 4496320.0))',32633) as b
	ON ST_Intersects(ST_Transform(a.geometry,32633), b.geometry)



SELECT ST_Intersection(ST_Transform(a.geometry,32633), b.geometry) as geometry
            FROM public.buildings a JOIN ST_GeomFromText('POLYGON((497560.0 4496320.0, 503660.0 4496320.0, 503660.0 4490220.0, 497560.0 4490220.0, 497560.0 4496320.0))',32633) as b
            ON ST_Intersects(ST_Transform(a.geometry,32633), b.geometry)
			ORDER BY a.index
			
			
-- DUPLICATE geometries
select * from (
	SELECT id, ROW_NUMBER() 
		OVER(PARTITION BY geom ORDER BY id asc) AS Row,
		geom FROM ONLY public.buildings
	) dups
	WHERE dups.Row > 1