from wof_solver3 import wof_solver

#

def test(pattern, attempted=None):
    result = wof_solver(pattern, attempted)

    print("\nPATTERN:", pattern)
    print("ATTEMPTED:", attempted)

    print("\nSOLUTIONS:")
    for s in result["solutions"][:10]:
        print("  ", s)

    print("\nTOP RANKED:")
    for s in result["ranked"][:10]:
        print("  ", s)

    print("\nNEXT BEST LETTER:", result["next_letter"])
    print("-" * 60)


if __name__ == "__main__":
    # Pattern from your example
    test("___ ___")

    # Test automatic attempted-letter inference
    test("C_MP_T_R PR_GR_MM_N_")

    # Test with no phrases.txt (delete/rename it to test)
    test("HEL__ W_R_D")

#    test("TO_TO___ _H_LL _Y_GLA____")

#    test("H___Y SH_P")