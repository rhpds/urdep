CREATE OR REPLACE TRIGGER urdep_inherit_subject_desired_state
  BEFORE INSERT OR UPDATE ON urdep_subject
  FOR EACH ROW
  EXECUTE FUNCTION urdep_inherit_subject_desired_state();
