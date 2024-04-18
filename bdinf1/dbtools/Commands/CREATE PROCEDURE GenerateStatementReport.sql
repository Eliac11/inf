CREATE PROCEDURE GenerateStatementReport @ReportParameter INT
AS
BEGIN
    
    CREATE TABLE #StatementReport (
        StatementId INT PRIMARY KEY,
        AccountId INT,
        OperationTypeId INT,
        OperationValue FLOAT,
        OperationDate DATE
    )

    
    INSERT INTO #StatementReport (StatementId, AccountId, OperationTypeId, OperationValue, OperationDate)
    SELECT
        s.intStatementId,
        s.intAccountId,
        o.intOperationTypeId,
        o.fltValue,
        o.datOperation
    FROM
        tblStatement s
    INNER JOIN
        tblOperation o ON s.intOperationId = o.intOperationId
    WHERE
        s.intReportId = @ReportParameter

    
    SELECT * FROM #StatementReport

    
    DROP TABLE #StatementReport
END