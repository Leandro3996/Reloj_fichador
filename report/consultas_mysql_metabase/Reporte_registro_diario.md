SELECT
  `source`.`ID Registro` AS `ID Registro`,
  `source`.`Hora Fichada` AS `Hora Fichada`,
  `source`.`Tipo de Movimiento` AS `Tipo de Movimiento`,
  `source`.`Tiempo de Descanso` AS `Tiempo de Descanso`,
  `source`.`Nombre Operario` AS `Nombre Operario`,
  `source`.`Apellido Operario` AS `Apellido Operario`,
  `source`.`Origen Fichada` AS `Origen Fichada`,
  `source`.`Inconsistencia` AS `Inconsistencia`,
  `source`.`Válido` AS `Válido`,
  `source`.`Descripción Inconsistencia` AS `Descripción Inconsistencia`
  
FROM
  (
    SELECT
      rd.id_registro AS "ID Registro",
      CONVERT_TZ(rd.hora_fichada, '+00:00', 'America/Argentina/Buenos_Aires') AS "Hora Fichada",
      CASE
        WHEN rd.tipo_movimiento = 'entrada' THEN 'Entrada'
        WHEN rd.tipo_movimiento = 'salida' THEN 'Salida'
        WHEN rd.tipo_movimiento = 'entrada_transitoria' THEN 'Entrada Transitoria'
        WHEN rd.tipo_movimiento = 'salida_transitoria' THEN 'Salida Transitoria'
        ELSE rd.tipo_movimiento
      END AS "Tipo de Movimiento",
      o.nombre AS "Nombre Operario",
      o.apellido AS "Apellido Operario",
      rd.origen_fichada AS "Origen Fichada",
      CASE
        WHEN rd.inconsistencia THEN '❌ Sí'
        ELSE '✅ No'
      END AS "Inconsistencia",
      CASE
        WHEN rd.valido THEN '✅ Sí'
        ELSE '❌ No'
      END AS "Válido",
      rd.descripcion_inconsistencia AS "Descripción Inconsistencia",
      CASE
        WHEN rd.tipo_movimiento = 'entrada_transitoria' THEN
          CONCAT(
            FLOOR(TIMESTAMPDIFF(SECOND, 
              (
                SELECT MAX(rd2.hora_fichada)
                FROM reloj_fichador_registrodiario rd2
                WHERE rd2.operario_id = rd.operario_id
                  AND rd2.tipo_movimiento = 'salida_transitoria'
                  AND rd2.hora_fichada < rd.hora_fichada
                  AND rd2.valido = TRUE
              ),
              rd.hora_fichada
            ) / 60), 'm ',
            MOD(TIMESTAMPDIFF(SECOND,
              (
                SELECT MAX(rd2.hora_fichada)
                FROM reloj_fichador_registrodiario rd2
                WHERE rd2.operario_id = rd.operario_id
                  AND rd2.tipo_movimiento = 'salida_transitoria'
                  AND rd2.hora_fichada < rd.hora_fichada
                  AND rd2.valido = TRUE
              ),
              rd.hora_fichada
            ), 60), 's'
          )
        ELSE NULL
      END AS "Tiempo de Descanso"
    FROM
      reloj_fichador_registrodiario rd
      JOIN reloj_fichador_operario o ON rd.operario_id = o.id
    LIMIT 1048575
  ) AS `source`
ORDER BY
  `source`.`Hora Fichada` DESC
LIMIT
  1048575