print("type togglemem is array (0 to 511) of std_logic_vector (511 downto 0);")
print("constant togglememory : togglemem := (")

for i in range(0, 512):
    val = ""
    for j in range(0, 511 - i):
        val = val + "0"

    val = val + "1"

    for j in range(512 - i, 512):
        val = val + "0"

    if i == 511:
        print("  ", i, " => \"", val, "\"", sep="")
    else:
        print("  ", i, " => \"", val, "\",", sep="")

print(");")
