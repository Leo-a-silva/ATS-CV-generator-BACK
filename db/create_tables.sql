-- USER
CREATE TABLE public.User
(
	id                BIGSERIAL NOT NULL DEFAULT nextval('app_user_id_seq'::regclass),
	email_address     CHARACTER (100) NOT NULL,
	created_at        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	password_hash     TEXT NOT NULL,
	CONSTRAINT app_user_pkey PRIMARY KEY (id)
	CONSTRAINT unique_email_address UNIQUE (email_address)
);

CREATE UNIQUE INDEX app_user_pkey ON public.User USING BTREE (id);

-- CV
CREATE TABLE public.Cv
(
	id                BIGSERIAL NOT NULL DEFAULT nextval('Cv_id_seq'::regclass),
	first_name        CHARACTER (50) NOT NULL,
	last_name         CHARACTER (50) NOT NULL,
	email_address     CHARACTER VARYING (150),
	phone_number      CHARACTER (20) NOT NULL,
	linkedin_url      TEXT NOT NULL,
	portfolio_url     TEXT NOT NULL,
	country           CHARACTER (80) NOT NULL,
	city              CHARACTER (80) NOT NULL,
	summary           TEXT NOT NULL,
	updated_at        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	created_at        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	user_id           BIGINT NOT NULL,
	CONSTRAINT Cv_pkey PRIMARY KEY (id)
);

ALTER TABLE public.Cv ADD CONSTRAINT Cv_User_id_fkey FOREIGN KEY (user_id) REFERENCES public.User (id);

CREATE UNIQUE INDEX Cv_pkey ON public.Cv USING BTREE (id);

-- WORK EXPERIENCE
CREATE TABLE public.Work Experience
(
	id               BIGSERIAL NOT NULL DEFAULT nextval('Work Experience_id_seq'::regclass),
	role             CHARACTER (80) NOT NULL,
	end_date         DATE,
	company_name     CHARACTER (100) NOT NULL,
	start_date       DATE NOT NULL,
	summary          TEXT NOT NULL,
	cv_id            BIGINT NOT NULL,
	CONSTRAINT Work Experience_pkey PRIMARY KEY (id)
);

ALTER TABLE public.Work Experience ADD CONSTRAINT Work Experience_Cv_id_fkey FOREIGN KEY (cv_id) REFERENCES public.Cv (id);

CREATE UNIQUE INDEX Work Experience_pkey ON public.Work Experience USING BTREE (id);

-- EDUCATION
CREATE TABLE public.Education
(
	id              BIGSERIAL NOT NULL DEFAULT nextval('Education_id_seq'::regclass),
	start_date      DATE NOT NULL,
	title           CHARACTER VARYING (63) NOT NULL,
	institution     CHARACTER VARYING (63) NOT NULL,
	end_date        DATE,
	cv_id           BIGINT NOT NULL,
	CONSTRAINT Education_pkey PRIMARY KEY (id)
);

ALTER TABLE public.Education ADD CONSTRAINT Education_Cv_id_fkey FOREIGN KEY (cv_id) REFERENCES public.Cv (id);

CREATE UNIQUE INDEX Education_pkey ON public.Education USING BTREE (id);

-- COURSES
CREATE TABLE public.Courses
(
	id              BIGSERIAL NOT NULL DEFAULT nextval('Courses_id_seq'::regclass),
	title           CHARACTER VARYING (10),
	date            DATE,
	institution     CHARACTER VARYING (63),
	cv_id           BIGINT NOT NULL,
	CONSTRAINT Courses_pkey PRIMARY KEY (id)
);

ALTER TABLE public.Courses ADD CONSTRAINT Courses_Cv_id_fkey FOREIGN KEY (cv_id) REFERENCES public.Cv (id);

CREATE UNIQUE INDEX Courses_pkey ON public.Courses USING BTREE (id);

-- SKILLS
CREATE TABLE public.Skills
(
	id        BIGSERIAL NOT NULL DEFAULT nextval('Skills_id_seq'::regclass),
	title     CHARACTER VARYING (10),
	cv_id     BIGINT NOT NULL,
	CONSTRAINT Skills_pkey PRIMARY KEY (id)
);

ALTER TABLE public.Skills ADD CONSTRAINT Skills_Cv_id_fkey FOREIGN KEY (cv_id) REFERENCES public.Cv (id);

CREATE UNIQUE INDEX Skills_pkey ON public.Skills USING BTREE (id);