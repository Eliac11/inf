CREATE PROCEDURE usp_CreateTempTableAndPopulate
AS
BEGIN

    IF OBJECT_ID('tempdb..#TempAccountOperations') IS NULL
    BEGIN
        CREATE TABLE #TempAccountOperations (
            AccountNumber NVARCHAR(20),
            OperationCount INT
        )
    END
    
    INSERT INTO #TempAccountOperations (AccountNumber, OperationCount)
    SELECT
        a.txtAccountNumber AS AccountNumber,
        COUNT(o.intOperationId) AS OperationCount
    FROM
        tblAccount a
    LEFT JOIN
        tblOperation o ON a.intAccountId = o.intAccountId
    GROUP BY
        a.txtAccountNumber

    
    SELECT * FROM #TempAccountOperations

END