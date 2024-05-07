-- name: get-pg-version^
SELECT metric_value FROM collection_postgres_calculated_metrics WHERE metric_name='VERSION';

-- name: insert-readiness-check!
INSERT INTO alloydb_readiness_check_summary (severity, assessment_type, info) VALUES (:severity, :assessment_type, :info);

--name: is-source-rds^
SELECT 
    CASE WHEN EXISTS
    (
        SELECT * FROM collection_postgres_extensions WHERE extension_owner='rdsadmin' AND is_super_user
    )
    THEN true
    ELSE false
END;

-- name: verify-collation-support!
INSERT INTO alloydb_readiness_check_summary (severity, assessment_type, info)
SELECT 'ERROR', 'UNSUPPORTED_DATABASE_LOCALE',
    CONCAT('Unsupported collation: ', c.collation, ' is not supported on this instance')
FROM collection_postgres_used_collations c
where c.collation NOT IN (%s);