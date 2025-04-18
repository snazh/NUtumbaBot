relationship = """
    CREATE TABLE relationship (
    user1 INTEGER,
    user2 INTEGER,
    love_status BOOLEAN NOT NULL,

    CONSTRAINT relationship_pkey PRIMARY KEY (user1, user2),
    CONSTRAINT relationship_user1_fkey FOREIGN KEY (user1) REFERENCES public.users (id),
    CONSTRAINT relationship_user2_fkey FOREIGN KEY (user2) REFERENCES public.users (id)
);
"""

evaluation: str = """


"""

user: str = """
"""
