
IF OBJECT_ID('dbo.Users', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Users
    (
        user_id INT IDENTITY(1,1) PRIMARY KEY,

        username NVARCHAR(100) NOT NULL,
        email NVARCHAR(255) NOT NULL,
        password_hash NVARCHAR(255) NOT NULL,

        role NVARCHAR(20) NOT NULL
            CONSTRAINT DF_Users_Role DEFAULT 'Viewer',

        is_active BIT NOT NULL
            CONSTRAINT DF_Users_IsActive DEFAULT 1,

        created_at DATETIME2 NOT NULL
            CONSTRAINT DF_Users_CreatedAt DEFAULT SYSUTCDATETIME(),

        updated_at DATETIME2 NULL,

        CONSTRAINT UQ_Users_Username UNIQUE (username),
        CONSTRAINT UQ_Users_Email UNIQUE (email),

        CONSTRAINT CK_Users_Role
            CHECK (role IN ('Admin', 'Analyst', 'Viewer'))
    );
END;
GO
