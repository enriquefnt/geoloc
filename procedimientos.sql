
DELIMITER $$
--
-- Procedimientos
--
DROP PROCEDURE IF EXISTS `controlesXcaso`$$
$$

DROP PROCEDURE IF EXISTS `datosGrafica`$$
$$

DROP PROCEDURE IF EXISTS `nominal`$$
$$

--
-- Funciones
--
DROP FUNCTION IF EXISTS `ZSCORE`$$
CREATE DEFINER=`saltaped`@`localhost` FUNCTION `ZSCORE` (`sexo` INT(1), `bus` VARCHAR(1), `valor` DOUBLE, `fecha_nace` DATE, `fecha_control` DATE) RETURNS DOUBLE READS SQL DATA BEGIN
    DECLARE calculo_z, L, M, S DOUBLE;
    DECLARE edad_mes, edad_dias INT;
    SET edad_mes = TIMESTAMPDIFF(MONTH, fecha_nace, fecha_control);
    SET edad_dias = TIMESTAMPDIFF(DAY, fecha_nace, fecha_control);
    IF (edad_dias < 1875 AND sexo = 2 AND bus = 'p') THEN
        SELECT la, ma, sa INTO L, M, S FROM tablaPEx WHERE age = edad_dias;
    ELSEIF (edad_dias < 1875 AND sexo = 2 AND bus = 't') THEN
        SELECT la, ma, sa INTO L, M, S FROM tablaTEx WHERE age = edad_dias;
    ELSEIF (edad_dias < 1875 AND sexo = 2 AND bus = 'i') THEN
        SELECT la, ma, sa INTO L, M, S FROM tablaIMCx WHERE age = edad_dias;
    ELSEIF (edad_dias < 1875 AND sexo = 1 AND bus = 'p') THEN
        SELECT lo, mo, so INTO L, M, S FROM tablaPEx WHERE age = edad_dias;
    ELSEIF (edad_dias < 1875 AND sexo = 1 AND bus = 't') THEN
        SELECT lo, mo, so INTO L, M, S FROM tablaTEx WHERE age = edad_dias;
    ELSEIF (edad_dias < 1875 AND sexo = 1 AND bus = 'i') THEN
        SELECT lo, mo, so INTO L, M, S FROM tablaIMCx WHERE age = edad_dias;
    ELSEIF (edad_mes > 59 AND sexo = 2 AND bus = 'p') THEN
        SELECT la, ma, sa INTO L, M, S FROM tablaPE6x WHERE age_s = edad_mes;
    ELSEIF (edad_mes > 59 AND sexo = 2 AND bus = 't') THEN
        SELECT la, ma, sa INTO L, M, S FROM tablaTE6x WHERE age_s = edad_mes;
    ELSEIF (edad_mes > 59 AND sexo = 2 AND bus = 'i') THEN
        SELECT la, ma, sa INTO L, M, S FROM tablaIMCE6x WHERE age_s = edad_mes;
    ELSEIF (edad_mes > 59 AND sexo = 1 AND bus = 'p') THEN
        SELECT lo, mo, so INTO L, M, S FROM tablaPE6x WHERE age_s = edad_mes;
    ELSEIF (edad_mes > 59 AND sexo = 1 AND bus = 't') THEN
        SELECT lo, mo, so INTO L, M, S FROM tablaTE6x WHERE age_s = edad_mes;
    ELSEIF (edad_mes > 59 AND sexo = 1 AND bus = 'i') THEN
        SELECT lo, mo, so INTO L, M, S FROM tablaIMCE6x WHERE age_s = edad_mes;
    ELSE
        SET L = NULL;
        SET M = NULL;
        SET S = NULL;
    END IF;
    IF L IS NULL OR M IS NULL OR S IS NULL THEN
        RETURN NULL;
    ELSE
        SET calculo_z = (POWER((valor/M), L) - 1) / (L * S);
        RETURN calculo_z;
    END IF;
END$$

DROP FUNCTION IF EXISTS `ZSCOREpt`$$
CREATE DEFINER=`saltaped`@`localhost` FUNCTION `ZSCOREpt` (`sexo` INT(1), `peso` DOUBLE, `medida` DOUBLE, `fecha_nace` DATE, `fecha_control` DATE) RETURNS DOUBLE READS SQL DATA BEGIN
    DECLARE calculo_z, L, M, S DOUBLE;
    DECLARE edad_dias INT;
    SET edad_dias = TIMESTAMPDIFF(DAY, fecha_nace, fecha_control);
    IF (edad_dias <= 730 AND sexo = 2 ) THEN
        SELECT la, ma, sa INTO L, M, S FROM tablaPesoLong WHERE talla = medida;
    ELSEIF (edad_dias <= 730 AND sexo = 1 ) THEN
        SELECT lo, mo, so INTO L, M, S FROM tablaPesoLong WHERE talla = medida;
    ELSEIF (edad_dias > 730 AND sexo = 2 ) THEN
        SELECT la, ma, sa INTO L, M, S FROM tablaPesoAltura WHERE talla = medida;
        ELSEIF (edad_dias > 730 AND sexo = 1 ) THEN
        SELECT lo, mo, so INTO L, M, S FROM tablaPesoAltura WHERE talla = medida;
       ELSE
        SET L = NULL;
        SET M = NULL;
        SET S = NULL;
    END IF;
    IF L IS NULL OR M IS NULL OR S IS NULL THEN
        RETURN NULL;
    ELSE
        SET calculo_z = (POWER((peso/M), L) - 1) / (L * S);
        RETURN calculo_z;
    END IF;
END$$

DELIMITER ;
