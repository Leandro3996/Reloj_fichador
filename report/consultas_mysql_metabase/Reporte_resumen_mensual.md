SELECT
    o.dni AS 'DNI',
    CONCAT(o.apellido, 
           IFNULL(CONCAT(' ', o.seg_apellido), ''), 
           ', ', 
           o.nombre, 
           IFNULL(CONCAT(' ', o.seg_nombre), '')
    ) AS 'Operario Apellido y nombre',
    ht.mes_actual AS 'Mes',
    -- Inconsistencias en el mes
    (SELECT COUNT(*) FROM reloj_fichador_registrodiario rd
        WHERE rd.operario_id = o.id
          AND rd.inconsistencia = 1
          AND DATE_FORMAT(rd.hora_fichada, '%Y-%m') = ht.mes_actual
    ) AS 'Inconsistencias',
    -- Inasistencias en el mes
    (SELECT COUNT(*) FROM reloj_fichador_registroasistencia ra
        WHERE ra.operario_id = o.id
          AND ra.estado_asistencia = 'ausente'
          AND DATE_FORMAT(ra.fecha, '%Y-%m') = ht.mes_actual
    ) AS 'Inasistencias',
    -- Justificadas
    (SELECT COUNT(*) FROM reloj_fichador_registroasistencia ra
        WHERE ra.operario_id = o.id
          AND ra.estado_asistencia = 'ausente'
          AND ra.estado_justificacion = 1
          AND DATE_FORMAT(ra.fecha, '%Y-%m') = ht.mes_actual
    ) AS 'Justificado',
    -- No justificadas
    (SELECT COUNT(*) FROM reloj_fichador_registroasistencia ra
        WHERE ra.operario_id = o.id
          AND ra.estado_asistencia = 'ausente'
          AND ra.estado_justificacion = 0
          AND DATE_FORMAT(ra.fecha, '%Y-%m') = ht.mes_actual
    ) AS 'No justificado',
    -- Licencia médica (días)
    IFNULL((
        SELECT SUM(DATEDIFF(
            IF(l.fecha_fin IS NULL, l.fecha_inicio, l.fecha_fin),
            l.fecha_inicio
        ) + 1)
        FROM reloj_fichador_licencia l
        WHERE l.operario_id = o.id
          AND DATE_FORMAT(l.fecha_inicio, '%Y-%m') = ht.mes_actual
    ), 0) AS 'Licencia médica (días)',
    -- Horas normales acumuladas en el mes
    CONCAT(
        CAST(FLOOR(ROUND(ht.horas_normales / 1000000) / 3600) AS CHAR), ' h ',
        CAST(FLOOR((ROUND(ht.horas_normales / 1000000) % 3600) / 60) AS CHAR), ' m'
    ) AS 'Horas Normales',
    -- Horas nocturnas acumuladas en el mes
    CONCAT(
        CAST(FLOOR(ROUND(ht.horas_nocturnas / 1000000) / 3600) AS CHAR), ' h ',
        CAST(FLOOR((ROUND(ht.horas_nocturnas / 1000000) % 3600) / 60) AS CHAR), ' m'
    ) AS 'Horas Nocturnas',
    -- Horas extras acumuladas en el mes
    CONCAT(
        CAST(FLOOR(ROUND(ht.horas_extras / 1000000) / 3600) AS CHAR), ' h ',
        CAST(FLOOR((ROUND(ht.horas_extras / 1000000) % 3600) / 60) AS CHAR), ' m'
    ) AS 'Horas Extras',
    -- Horas feriado acumuladas en el mes
    CONCAT(
        CAST(FLOOR(ROUND(ht.horas_feriado / 1000000) / 3600) AS CHAR), ' h ',
        CAST(FLOOR((ROUND(ht.horas_feriado / 1000000) % 3600) / 60) AS CHAR), ' m'
    ) AS 'Horas Feriado',
    -- Total de horas trabajadas en el mes (suma de todas)
    CONCAT(
        CAST(FLOOR(ROUND((ht.horas_normales + ht.horas_nocturnas + ht.horas_extras + ht.horas_feriado) / 1000000) / 3600) AS CHAR), ' h ',
        CAST(FLOOR((ROUND((ht.horas_normales + ht.horas_nocturnas + ht.horas_extras + ht.horas_feriado) / 1000000) % 3600) / 60) AS CHAR), ' m'
    ) AS 'Total de Horas en el Mes'
FROM
    reloj_fichador_horas_totales ht
JOIN
    reloj_fichador_operario o ON ht.operario_id = o.id
ORDER BY
    o.apellido, o.nombre, ht.mes_actual;