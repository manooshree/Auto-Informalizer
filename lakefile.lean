import Lake
open Lake DSL

package Informalizer {
  -- Add package configuration here
}


require mathlib from git "https://github.com/leanprover-community/mathlib4"
@[default_target]
lean_lib «Informalizer» {
  -- add any library configuration options here
}
