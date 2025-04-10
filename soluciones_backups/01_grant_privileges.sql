-- Otorgar privilegio PROCESS al usuario de MySQL para permitir los backups completos
GRANT PROCESS ON *.* TO 'Leandro.3996'@'%';
FLUSH PRIVILEGES; 