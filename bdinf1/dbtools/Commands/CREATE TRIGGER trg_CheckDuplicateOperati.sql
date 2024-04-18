CREATE TRIGGER trg_CheckDuplicateOperation
ON tblOperation
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1
        FROM inserted i
        INNER JOIN tblOperation o ON i.intAccountId = o.intAccountId AND i.datOperation = o.datOperation
        WHERE i.intOperationId <> o.intOperationId
    )
    BEGIN
        RAISERROR ('Duplicate operation', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END;
END;
