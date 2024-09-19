CREATE OR REPLACE FUNCTION urdep_inherit_subject_desired_state() RETURNS TRIGGER AS $$
  BEGIN
    IF NEW.parent_uuid IS NOT NULL THEN
      NEW.desired_state := (SELECT desired_state FROM urdep_subject WHERE uuid=NEW.parent_uuid);
    END IF;
  END;
$$ LANGUAGE plpgsql;
