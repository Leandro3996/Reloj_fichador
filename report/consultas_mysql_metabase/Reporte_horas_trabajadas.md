SELECT
  `source`.`Fecha` AS `Fecha`,
  `source`.`Mes` AS `Mes`,
  `source`.`Operario` AS `Operario`,
  `source`.`Horas Normales` AS `Horas Normales`,
  `source`.`Horas Nocturnas` AS `Horas Nocturnas`,
  `source`.`Horas Extras` AS `Horas Extras`,
  `source`.`Total de Horas` AS `Total de Horas`
FROM
  (
    SELECT
      t.`Fecha` AS "Fecha",
      DATE_FORMAT(t.`Fecha`, '%Y-%m') AS "Mes",
      t.`Operario` AS "Operario",
      t.`Horas Normales` AS "Horas Normales",
      t.`Horas Nocturnas` AS "Horas Nocturnas",
      t.`Horas Extras` AS "Horas Extras",
      t.`Total Horas` AS "Total de Horas"
    FROM
      (
        SELECT
          ht.`fecha` AS "Fecha",
          CONCAT(o.`apellido`, ', ', o.`nombre`) AS "Operario",
          SEC_TO_TIME(ROUND(ht.`horas_normales` / 1000000)) AS "Horas Normales",
          SEC_TO_TIME(ROUND(ht.`horas_nocturnas` / 1000000)) AS "Horas Nocturnas",
          SEC_TO_TIME(ROUND(ht.`horas_extras` / 1000000)) AS "Horas Extras",
          SEC_TO_TIME(
            ROUND(
              (
                ht.`horas_normales` + ht.`horas_nocturnas` + ht.`horas_extras`
              ) / 1000000
            )
          ) AS "Total Horas"
        FROM
          `reloj_fichador_horas_trabajadas` ht
          JOIN `reloj_fichador_operario` o ON ht.`operario_id` = o.`id`
      ) t
   
ORDER BY
      t.`Fecha` DESC,
      t.`Operario` ASC
   
LIMIT
      1048575
  ) AS `source`
LIMIT
  1048575