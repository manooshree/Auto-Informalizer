import Lean

open Lean Meta Elab Tactic


def runSuggest (goal : String) : IO String := do
  let cwd ← IO.currentDir
  let path := cwd / "translate.py"
  if ← path.pathExists then
    let result ← IO.Process.output {
      cmd := "python3"
      args := #[path.toString, goal]
    }
    return result.stdout.trim
  else
    throw <| IO.userError s!"Python script not found at {path.toString}"

def runSuggestMetaM (goal : String) : MetaM String := do
  return ← liftM <| runSuggest goal


def extractGoalMetaM (g : MVarId) : MetaM String := do
  let ppGoal ← Meta.ppGoal g
  return toString ppGoal


syntax "bt" tactic : tactic

elab_rules : tactic
  | `(tactic| bt $tac:tactic) => do
    -- goal before tactic
    let beforeGoal ← liftMetaMAtMain fun g => extractGoalMetaM g
    dbg_trace s!"Goal before tactic: {beforeGoal}"

    -- user tactic
    let tacticString := tac.raw.reprint.getD "unknown tactic"
    dbg_trace s!"User-provided tactic: {tac}"
    evalTactic tac

    -- goal after tactic
    let afterGoal ← liftMetaMAtMain fun g => extractGoalMetaM g
    dbg_trace s!"Goal after tactic: {afterGoal}"

    let combinedGoals := s!"Before:\n{beforeGoal}\n\nAfter:\n{afterGoal}\n\nTactic: {tacticString}"
    let output ← liftM <| runSuggest combinedGoals
    logInfo s!"Python script output: {output}"
