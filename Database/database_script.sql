BEGIN TRANSACTION;

DROP TABLE IF EXISTS newuser, meyersbriggs CASCADE; 


CREATE TABLE newuser (
	user_id serial PRIMARY KEY,
    username varchar(30) NOT NULL,
	birth_date date NOT NULL,
    password varchar(100) NOT NULL,
    created_dt timestamp NOT NULL DEFAULT now(),
    updated_dt timestamp NOT NULL DEFAULT now(),
    email varchar(100) NOT NULL,
	CONSTRAINT unique_user UNIQUE (user_id, email, username)
);

CREATE TABLE meyersbriggs (
	user_id int,
	extraversion int,
	introversion int,
	sensing int,
	intuition int,
	thinking int,
	feeling int,
	judging int,
	perceiving int,
    created_dt timestamp NOT NULL DEFAULT now(),
    updated_dt timestamp NOT NULL DEFAULT now(),
	CONSTRAINT FK_user_id FOREIGN KEY (user_id) REFERENCES newuser(user_id)
);

CREATE OR REPLACE FUNCTION update_updated_dt_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_dt = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

	
CREATE TRIGGER update_meyersbriggs_updated_dt
    BEFORE UPDATE ON meyersbriggs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_dt_column();
	
CREATE TRIGGER update_user_updated_dt
    BEFORE UPDATE ON newuser
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_dt_column();

--rollback
COMMIT;