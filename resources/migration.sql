ALTER TABLE todos ADD COLUMN completed INT(1);
UPDATE todos SET completed = 0;