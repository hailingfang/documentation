Experiment Language
=======================

.. code::

    def make_solid_solute_solution:
    (solvent, solute; beaker, volumetric_flask; $m Mol, $v ml)
    [solution:$m Mol:$v ml]
    >Reagents
    solvent: the meterial will be disolve.
    solute

    >tools
    beaker: container to dissolve solvent.
    volumetric_flask: used to quantify the molar concentrition.
    
    >quantity
    $m: the molar concentrition.
    $v: the volume of solution.

    <out
    solution

        #volumetric_flask, $v_falsk = <choose_container>(#volumetirc_flask; $v)

        $solvent_mass = $m * $v_falsk / 1000 * <Mol>(#solvent)
        #solvent_w = <weight>(#solvent; $solvent_mass)
        #solute_v = <volume>(#solute; 4/5 * $v)
        #solution_in_beaker = <disolve>(#solvent_w, #solute_v; #beaker)
        #solution_in_flask = <move>(#solution_in_beaker; #volumeric_flask)
        #solution = <volumetric_flask>(#solution_in_flask)
        #solution = <volume>(#solute; $v)
        
        return #solution
