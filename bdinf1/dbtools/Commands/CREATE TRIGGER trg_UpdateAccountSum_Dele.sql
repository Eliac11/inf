CREATE TRIGGER trg_UpdateAccountSum_Delete
ON tblOperation
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @AccountId INT;
    DECLARE @TotalValue FLOAT;

    
    DECLARE account_cursor CURSOR FOR
        SELECT DISTINCT intAccountId
        FROM deleted;

    OPEN account_cursor;
    FETCH NEXT FROM account_cursor INTO @AccountId;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        SELECT @TotalValue = SUM(fltValue)
        FROM tblOperation
        WHERE intAccountId = @AccountId;

        UPDATE tblAccount
        SET fltAccountSum = @TotalValue
        WHERE intAccountId = @AccountId;

        FETCH NEXT FROM account_cursor INTO @AccountId;
    END;

    CLOSE account_cursor;
    DEALLOCATE account_cursor;
END;