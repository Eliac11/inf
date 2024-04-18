CREATE PROCEDURE usp_CreateTempStatementTable
    @ReportParameter INT
AS
BEGIN

    IF OBJECT_ID('tempdb..#TempStatement') IS NULL
    BEGIN
        CREATE TABLE #TempStatement (
            OperationDate DATE,
            OperationDescription NVARCHAR(255),
            OperationAmount FLOAT
        )
    END

    INSERT INTO #TempStatement (OperationDate, OperationDescription, OperationAmount)
    SELECT
        datOperation AS OperationDate,
        CONCAT(ot.txtOperationTypeName, ' - ', a.txtAccountNumber) AS OperationDescription,
        op.fltValue AS OperationAmount
    FROM
        tblOperation op
    INNER JOIN
        tblOperationType ot ON op.intOperationTypeId = ot.intOperationTypeId
    INNER JOIN
        tblAccount a ON op.intAccountId = a.intAccountId
    WHERE
        a.intClientId = @ReportParameter

    SELECT * FROM #TempStatement

END