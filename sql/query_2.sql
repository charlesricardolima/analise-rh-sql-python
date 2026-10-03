-- Query 2 - Funcionários por Região
-- Relaciona funcionários aos seus departamentos e informações geográficas.
-- O filtro mantém apenas registros com região identificada.

SELECT
    funcionarios.EMPLOYEE_ID,
    funcionarios.FIRST_NAME,
    funcionarios.LAST_NAME,
    funcionarios.SALARY,
    departamentos.DEPARTMENT_NAME,
    localizacoes.STREET_ADDRESS,
    localizacoes.CITY,
    localizacoes.STATE_PROVINCE,
    paises.COUNTRY_NAME,
    regioes.REGION_NAME
FROM HR.EMPLOYEES funcionarios

LEFT JOIN HR.DEPARTMENTS departamentos
    ON funcionarios.DEPARTMENT_ID = departamentos.DEPARTMENT_ID

LEFT JOIN HR.LOCATIONS localizacoes
    ON departamentos.LOCATION_ID = localizacoes.LOCATION_ID

LEFT JOIN HR.COUNTRIES paises
    ON localizacoes.COUNTRY_ID = paises.COUNTRY_ID

LEFT JOIN HR.REGIONS regioes
    ON paises.REGION_ID = regioes.REGION_ID

WHERE regioes.REGION_NAME IS NOT NULL
ORDER BY regioes.REGION_NAME, funcionarios.EMPLOYEE_ID;