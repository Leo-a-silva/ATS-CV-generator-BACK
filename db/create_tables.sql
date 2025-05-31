-- USER
CREATE TABLE public.User
(
	id                SERIAL PRIMARY KEY,
	email_address     TEXT NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	password_hash     TEXT NOT NULL,
	CONSTRAINT unique_email_address UNIQUE (email_address)
);

-- CV
CREATE TABLE public.Cv
(
	id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email_address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    linkedin_url TEXT NOT NULL,
    portfolio_url TEXT NOT NULL,
    country VARCHAR(80) NOT NULL,
    city VARCHAR(80) NOT NULL,
    summary TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.Cv ADD CONSTRAINT Cv_User_id_fkey FOREIGN KEY (user_id) REFERENCES public.User (id);