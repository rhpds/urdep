CREATE OR REPLACE TRIGGER urdep_propagate_subject_desired_state
  AFTER INSERT OR UPDATE ON urdep_subject
  FOR EACH ROW
  EXECUTE FUNCTION urdep_propagate_subject_desired_state();
