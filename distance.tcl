set work_dir [lindex $argv 0]
set output [lindex [split $work_dir /] end-1]

set atom_name "name CA and resname HIE HID HSD HSE HIS"
set molid [mol new ${work_dir}/wrap.pdb]
set atoms [atomselect top "$atom_name"]
set atom_ids [lsort -integer [$atoms get index]]
set atom_ids "196 220 432"

if ![file exist data] {file mkdir data}
set output [open data/${output}.tsv w]
foreach trj [lsort [glob ${work_dir}/*.trr]] {
    set trjname [lindex [split $trj /.] end-1]
    animate delete all
    mol addfile ${trj} waitfor all
    puts "calculating ${trj}"
    set numframes [molinfo $molid get numframes]
    # for GROMACS, the last trj frame should be dropped
    for {set frame 0} {$frame < [expr $numframes - 1]} {incr frame} {
        puts -nonewline $output [format "%15s\t%8d" $trjname $frame]
        foreach atom_id1 $atom_ids {
                foreach atom_id2 $atom_ids {
                    if {$atom_id1 == $atom_id2} {continue}
                    puts -nonewline $output [format "\t%8.4f" [measure bond "$atom_id1 $atom_id2" frame $frame]]
                }
        }
        puts -nonewline $output "\n"
    }
}
close $output
exit
