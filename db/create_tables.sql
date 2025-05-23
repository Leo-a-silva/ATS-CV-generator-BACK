
-- user

CREATE TABLE public.User
(
	id                BIGSERIAL NOT NULL DEFAULT nextval('app_user_id_seq'::regclass),
	first_name        TEXT NOT NULL,
	email_address     CHARACTER (100) NOT NULL,
	created_at        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	updated_at        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	password_hash     TEXT NOT NULL,
	last_name         TEXT NOT NULL,
	CONSTRAINT app_user_pkey PRIMARY KEY (id)
);

CREATE UNIQUE INDEX app_user_pkey ON public.User USING BTREE (id);

-- cv

CREATE TABLE public.cv
(
	id                   BIGSERIAL NOT NULL DEFAULT nextval('CV_id_seq'::regclass),
	telephone_number     BIGINT,
	role                 CHARACTER VARYING (30) NOT NULL,
	summary              TEXT NOT NULL,
	user_id              BIGINT NOT NULL,
	created_at           TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	updated_at           TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	contact_email        CHARACTER (100) NOT NULL,
	social_link_1        TEXT,
	social_link_2        TEXT,
	CONSTRAINT CV_pkey PRIMARY KEY (id)
);

ALTER TABLE public.cv ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.User (id);

CREATE UNIQUE INDEX CV_pkey ON public.cv USING BTREE (id);

-- skill

CREATE TABLE public.skill
(
	id             BIGSERIAL NOT NULL DEFAULT nextval('skills_id_seq'::regclass),
	cv_id          BIGINT NOT NULL,
	title          CHARACTER VARYING (10),
	updated_at     TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	created_at     TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	level          CHARACTER (50),
	CONSTRAINT skills_pkey PRIMARY KEY (id)
);

ALTER TABLE public.skill ADD CONSTRAINT cv_id FOREIGN KEY (cv_id) REFERENCES public.cv (id);

CREATE UNIQUE INDEX skills_pkey ON public.skill USING BTREE (id);

-- work experience

CREATE TABLE public.work_experience
(
	id               BIGSERIAL NOT NULL DEFAULT nextval('work_experience_id_seq'::regclass),
	cv_id            BIGINT NOT NULL,
	created_at       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	start_date       DATE NOT NULL,
	end_date         DATE,
	updated_at       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	company_name     CHARACTER (80) NOT NULL,
	description      TEXT NOT NULL,
	CONSTRAINT work_experience_pkey PRIMARY KEY (id)
);

ALTER TABLE public.work_experience ADD CONSTRAINT cv_id FOREIGN KEY (cv_id) REFERENCES public.cv (id);

CREATE UNIQUE INDEX work_experience_pkey ON public.work_experience USING BTREE (id);

-- certification

CREATE TABLE public.certification
(
	id              BIGSERIAL NOT NULL DEFAULT nextval('certifications_id_seq'::regclass),
	name            CHARACTER VARYING (63),
	institution     CHARACTER VARYING (63),
	date            DATE,
	cv_id           BIGINT NOT NULL,
	updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	description     TEXT,
	CONSTRAINT certifications_pkey PRIMARY KEY (id)
);

ALTER TABLE public.certification ADD CONSTRAINT cv_id FOREIGN KEY (cv_id) REFERENCES public.cv (id);

CREATE UNIQUE INDEX certifications_pkey ON public.certification USING BTREE (id);

-- academic

CREATE TABLE public.academic
(
	id              BIGSERIAL NOT NULL DEFAULT nextval('academic_id_seq'::regclass),
	title           CHARACTER VARYING (63) NOT NULL,
	institution     CHARACTER VARYING (63) NOT NULL,
	start_date      DATE NOT NULL,
	cv_id           BIGINT NOT NULL,
	end_date        DATE,
	updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	description     TEXT,
	CONSTRAINT academic_pkey PRIMARY KEY (id)
);

ALTER TABLE public.academic ADD CONSTRAINT cv_id FOREIGN KEY (cv_id) REFERENCES public.cv (id);

CREATE UNIQUE INDEX academic_pkey ON public.academic USING BTREE (id);

-- language

CREATE TABLE public.language
(
	id                BIGSERIAL NOT NULL DEFAULT nextval('Languages_id_seq'::regclass),
	language_name     CHARACTER VARYING (30) NOT NULL,
	cv_id             BIGINT NOT NULL,
	created_at        TIMESTAMP WITH TIME ZONE,
	updated_at        TIMESTAMP WITH TIME ZONE,
	level             CHARACTER (50),
	certificate       CHARACTER VARYING (30),
	CONSTRAINT Languages_pkey PRIMARY KEY (id)
);

ALTER TABLE public.language ADD CONSTRAINT cv_id FOREIGN KEY (cv_id) REFERENCES public.cv (id);

CREATE UNIQUE INDEX Languages_pkey ON public.language USING BTREE (id);

-- project

CREATE TABLE public.project
(
	id              BIGSERIAL NOT NULL DEFAULT nextval('project_id_seq'::regclass),
	cv_id           BIGINT NOT NULL,
	title           CHARACTER VARYING (63),
	tech_stack      TEXT,
	description     TEXT,
	updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	link            TEXT,
	CONSTRAINT project_pkey PRIMARY KEY (id)
);

ALTER TABLE public.project ADD CONSTRAINT project_cv_id_fkey FOREIGN KEY (cv_id) REFERENCES public.cv (id);

CREATE UNIQUE INDEX project_pkey ON public.project USING BTREE (id);
