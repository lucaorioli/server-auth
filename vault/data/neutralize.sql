-- remove the encrypted secrets, files and inbox entries; vaults, entries, rights and
-- user keys are kept so that the neutralized database stays usable for testing
DELETE FROM vault_field;
DELETE FROM vault_file;
DELETE FROM vault_inbox;
