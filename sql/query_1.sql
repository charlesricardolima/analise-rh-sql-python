-- Query 1 - Salários por Departamento e Cargo
-- Relaciona funcionários com seus departamentos e cargos.
-- O filtro considera apenas salários positivos.

SELECT
    funcionarios.EMPLOYEE_ID,
    funcionarios.FIRST_NAME,
    funcionarios.LAST_NAME,
    funcionarios.SALARY,
    departamentos.DEPARTMENT_NAME,
    cargos.JOB_TITLE
FROM HR.EMPLOYEES funcionarios

LEFT JOIN HR.DEPARTMENTS departamentos
    ON funcionarios.DEPARTMENT_ID = departamentos.DEPARTMENT_ID

LEFT JOIN HR.JOBS cargos
    ON funcionarios.JOB_ID = cargos.JOB_ID

WHERE funcionarios.SALARY > 0
ORDER BY funcionarios.EMPLOYEE_ID;