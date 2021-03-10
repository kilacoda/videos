from chanim import *
# from periodic_table import PeriodicTable

OUTPUT_DIRECTORY = "KilaCoda/markovnikoff"
config.tex_template = TexTemplateLibrary.simple

## Silly common constructs
class InductiveArrows(VMobject):
    """Arrows indicating an inductive effect

    Arguments:
        num_arrows -- The number of arrows you want.
        arrange_direction -- The direction which the arrows pointy-pointy towards.
    Returns:
        [type] -- [description]
    """
    CONFIG = {
        "num_arrows":1,
        "arrange_direction":RIGHT
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for i in range(self.num_arrows):
            self.add(
                VGroup(
                    Line(UP,RIGHT),Line(RIGHT,DOWN)
                ).arrange(DOWN,buff=0).scale(0.25)
            )

        self.scale(0.5)
        self.arrange(self.arrange_direction,buff=0.1)

    def rotating_effect(self):
        for head in self:
            head.rotate(PI/2)


        return [
            ApplyMethod(head.rotate,-PI/2)
            for head in self
        ]

    def fade_in_one_by_one(self):
        return LaggedStartMap(
            FadeInFrom,self
        )

## Other Scenes
class IntroBadJoke(Scene):
    def construct(self):
        self.intro_bad_joke()


    def intro_bad_joke(self):
        HBr = ChemObject("H-Br")
        arrow_1 = CArrow()
        H_OH = ChemObject("H-OH")

        questionable_reaction_grp = VGroup(HBr.copy(),arrow_1,H_OH)
        questionable_reaction_grp.arrange(RIGHT)

        q_mark = TextMobject("?").scale(1.5).shift(UP/2+LEFT*0.35)

        self.play(Write(HBr));self.wait()

        self.play(
            Transform(HBr,questionable_reaction_grp)
        );self.wait()

        self.play(FadeIn(q_mark));self.wait()

        self.play(ShowCreation(Cross(VGroup(*self.mobjects)).shift(DOWN*0.25)));self.wait(2)

        consolation = TextMobject("But there is something similar.").to_edge(DOWN,1.5)

        self.play(FadeInFrom(consolation));self.wait(3)


class TitleScene(Scene):
    def construct(self):
        vid_tit = TextMobject("\\huge{Markovnikov's Rule} \\\\"," \\tiny{for Organic substitution reactions}");
        vid_tit[0].set_color(RED);
        moi = TextMobject("By KilaCoda Animations");

        test_obj = Square().set_opacity(0)
        self.add(test_obj)

        VGroup(vid_tit,moi).arrange(DOWN,buff=1.25)

        self.wait(2)
        self.add(vid_tit);self.wait(2)
        self.add(moi);self.wait(2)

class AlcoholsArePrettyImportant(Scene):

    CONFIG = {

        "chems_and_names":{
            "CH_3 OH":"Methanol",
            "CH_3 CH_2 OH":"Ethanol",
            "CH_2(-[6]OH)-CH_2(-[6]OH)":"Ethylene Glycol",
            "CH_3-CH(-[6]OH)-CH_3":"Isopropyl Alcohol",
            "CH_2OH(-[-2]CHOH(-[-2]CH_2 OH))":"Glycerol"
        }

    }



    def construct(self):
        alc_general = ChemWithName("R-OH","Alcohols")
        self.play(alc_general.creation_anim());self.wait(2)

        self.play(
            ApplyMethod(alc_general.arrange,RIGHT),
        )

        self.play(
            ApplyMethod(alc_general.to_edge,UP),
        )

        underline = Underline(alc_general)
        self.play(Write(underline));self.wait(2)

        examples = self.get_examples()

        arranged_examples = VGroup(
            examples[0:3].arrange(RIGHT,buff=2),examples[3:].arrange(RIGHT,buff=2)
        ).arrange(DOWN,buff=1.1).shift(DOWN*0.5)

        for index,ex in enumerate(examples):
            self.play(ex.creation_anim());self.wait()
            if index in (0,1,2):
                row,column=0,index
            else:
                row,column=1,index-3
            print(index,row,column)
            self.play(ex.move_to,arranged_examples[row][column])

        self.wait(3)

    def get_vgroup_of_chemnames_and_usages(self,chems:list,names:list,usages:list):
        try:
            assert(len(chems)==len(names)==len(usages))
        except AssertionError:
            raise Exception("Lengths of all three lists should be equal.")

        cases = VGroup()
        for chem,name,usage in zip(chems,names,usages):
            cases.add(
                VGroup(
                    ChemWithName(chem,name),CArrow(),TextMobject(usage)
                ).arrange(RIGHT)
            )

        return cases

    def get_examples(self):
        chems_and_names = self.chems_and_names
        examples = VGroup()

        for chem in chems_and_names:
            examples.add(ChemWithName(chem,chems_and_names[chem]).scale(0.75))
        return examples


class NormalMarksAddition(Scene):
    def construct(self):
        example = Reaction(
            ["CH_2 = CH - CH_3"],
            ["CH_2(-[-2]H) - CH_2 (-[-2]Br) - CH_3"],
            arrow_text_up="\\chemfig{H-Br}",
            arrow_length=1.5
        )

        # intermediates = [
        #     ChemObject("")
        # ]
        example[-1].shift(DOWN*0.5)

        self.play(FadeInFrom(example[:-1]));self.wait()
        # self.add(get_submobject_index_labels(example[0]))
        # print_family(example[0])
        sbe = split_bond_electrons =VGroup(SmallDot(),SmallDot()).arrange(RIGHT,buff=0.15).set_color(YELLOW)
        breaker = BondBreak(example[0][5],length=0.45,color=YELLOW)
        self.play(ShowCreation(breaker))
        self.play(
            ReplacementTransform(
                example[0][5],
                split_bond_electrons,
                move_to=True
            ),
            Uncreate(breaker)
        );self.wait()

        sbe_HBr = split_bond_electrons_HBr = VGroup(SmallDot(),SmallDot()).arrange(RIGHT,buff=0.15).set_color(RED)
        HBr_breaker = BondBreak(example[1][7],color=RED)
        self.play(
            ShowCreation(HBr_breaker)
        );self.play(
            ReplacementTransform(
                example[1][7],split_bond_electrons_HBr,move_to=True
            )
        )

        footnote = TextMobject("* The split HBr atoms shown here are not radicals, but rather ions! \\\\ This is an attempt to visualise the basic concept behind this rule; the mechanism follows after.").to_corner()
        footnote.scale(0.5)
        self.add(footnote)
        self.wait(0.5)
        self.remove(footnote)
        self.play(
            split_bond_electrons[0].shift,UL*0.5 + LEFT*0.4 +DOWN*0.1,
            split_bond_electrons[1].shift,UR*0.5 + DOWN*0.1 +LEFT*0.15,
            example[0][6].shift,UP*0.09,
            Uncreate(HBr_breaker)
        );self.wait()

        H_rad = VGroup(
            example[1][4],
            sbe_HBr[0]
        )

        Br_rad = VGroup(
            example[1][5:7],
            sbe_HBr[1]
        )
        self.play(
            H_rad.arrange,DOWN,
            H_rad.next_to,sbe[0],UP,buff=0.75
        );self.play(
            Br_rad.arrange,DOWN,
            Br_rad.next_to,sbe[1],UP,buff=0.75
        );self.wait()

        final = VGroup(
            sbe,H_rad,Br_rad,example[0][:5],example[0][6:]
        )

        self.play(
            FadeOut(example[1][0:4  ]),
            final.center
        );self.wait(2)

        final_descriptor_bonds = VGroup(
            Line(
                    sbe[0].get_center(),
                    sbe_HBr[0].get_center()
            ),
            Line(
                    sbe[1].get_center(),
                    sbe_HBr[1].get_center()
            )
        )
        self.play(
            ShowCreation(
                final_descriptor_bonds
            ),

            FadeOut(sbe),FadeOut(sbe_HBr)
        );self.wait()

        cleaner_final = ChemWithName(
            "CH_3 - CH (-[2]Br) - CH_3",
            "2-bromopropane"
        )

        self.play(
            Transform(
                final,cleaner_final.chem
            ),
            FadeInFrom(cleaner_final.name),
            FadeOut(final_descriptor_bonds)
        );self.wait(2)

class NormalMarksAdditionWithoutFootnote(Scene):
    def construct(self):
        example = Reaction(
            ["CH_2 = CH - CH_3"],
            ["CH_2(-[-2]H) - CH_2 (-[-2]Br) - CH_3"],
            arrow_text_up="\\chemfig{H-Br}",
            arrow_length=1.5
        )

        # intermediates = [
        #     ChemObject("")
        # ]
        example[-1].shift(DOWN*0.5)

        self.play(FadeInFrom(example[:-1]));self.wait()
        # self.add(get_submobject_index_labels(example[0]))
        # print_family(example[0])
        sbe = split_bond_electrons =VGroup(SmallDot(),SmallDot()).arrange(RIGHT,buff=0.15).set_color(YELLOW)
        breaker = BondBreak(example[0][5],length=0.45,color=YELLOW)
        self.play(ShowCreation(breaker))
        self.play(
            ReplacementTransform(
                example[0][5],
                split_bond_electrons,
                move_to=True
            ),
            Uncreate(breaker)
        );self.wait()

        sbe_HBr = split_bond_electrons_HBr = VGroup(SmallDot(),SmallDot()).arrange(RIGHT,buff=0.15).set_color(RED)
        HBr_breaker = BondBreak(example[1][7],color=RED)
        self.play(
            ShowCreation(HBr_breaker)
        );self.play(
            ReplacementTransform(
                example[1][7],split_bond_electrons_HBr,move_to=True
            )
        )

        footnote = TextMobject("* The split HBr atoms shown here are not radicals, but rather ions! \\\\ This is an attempt to visualise the basic concept behind this rule; the mechanism follows after.").to_corner()
        footnote.scale(0.5)
        ##self.add(footnote)
        ##self.wait(0.5)
        ##self.remove(footnote)
        self.play(
            split_bond_electrons[0].shift,UL*0.5 + LEFT*0.4 +DOWN*0.1,
            split_bond_electrons[1].shift,UR*0.5 + DOWN*0.1 +LEFT*0.15,
            example[0][6].shift,UP*0.09,
            Uncreate(HBr_breaker)
        );self.wait()

        H_rad = VGroup(
            example[1][4],
            sbe_HBr[0]
        )

        Br_rad = VGroup(
            example[1][5:7],
            sbe_HBr[1]
        )
        self.play(
            H_rad.arrange,DOWN,
            H_rad.next_to,sbe[0],UP,buff=0.75
        );self.play(
            Br_rad.arrange,DOWN,
            Br_rad.next_to,sbe[1],UP,buff=0.75
        );self.wait()

        final = VGroup(
            sbe,H_rad,Br_rad,example[0][:5],example[0][6:]
        )

        self.play(
            FadeOut(example[1][0:4  ]),
            final.center
        );self.wait(2)

        final_descriptor_bonds = VGroup(
            Line(
                    sbe[0].get_center(),
                    sbe_HBr[0].get_center()
            ),
            Line(
                    sbe[1].get_center(),
                    sbe_HBr[1].get_center()
            )
        )
        self.play(
            ShowCreation(
                final_descriptor_bonds
            ),

            FadeOut(sbe),FadeOut(sbe_HBr)
        );self.wait()

        cleaner_final = ChemWithName(
            "CH_3 - CH (-[2]Br) - CH_3",
            "2-bromopropane"
        )

        self.play(
            Transform(
                final,cleaner_final.chem
            ),
            FadeInFrom(cleaner_final.name),
            FadeOut(final_descriptor_bonds)
        );self.wait(2)


## Mechanism Steps
class StepsScene(Scene):
    CONFIG = {
        "title":"Steps:",
        "title_corner":UP+LEFT,
        "title_to_corner_buff":1.5,
        "title_scale_factor":1.4,
        "steps":[],
        "unfaded_index":None,
        "steps_play_animation":FadeInFrom,
        "add_steps_one_by_one":True,
        "play_or_add_steps":"play"
    }

    def construct(self):
        pass

    def add_title(self):
        if not isinstance(self.title,TextMobject):
            title = self.title = TextMobject(self.title)

        else:
            title = self.title

        title.scale(1.4).to_corner(UP+LEFT,1.5)

        self.add(title)

    def add_steps(self):
        steps = self.steps = BulletedList(*self.steps)

        if not self.add_steps_one_by_one:
            if self.play_or_add_steps=="play":
                self.play(self.steps_play_animation(steps))
            elif self.play_or_add_steps=="add":
                self.add(steps)

        else:
            for step in steps:
                if self.play_or_add_steps=="play":
                    self.play(self.steps_play_animation(step));self.wait()
                elif self.play_or_add_steps=="add":
                    self.add(step)

    def fade_all_steps_except_index(self,wait_time=DEFAULT_WAIT_TIME):
        if self.unfaded_index is None:
            self.unfaded_index = 0

        self.play(self.steps.fade_all_but,self.unfaded_index)
        self.wait(wait_time)

class ShowMechanismSteps(StepsScene):
    CONFIG = {
        "steps": [
            "Electrophile production (from hydrogen halide)",
            "Carbocation formation",
            "Attack of nucleophile"
        ]
    }
    def construct(self):
        self.add_title()
        self.add_steps()
        # self.fade_all_steps_except_index()

class EmphasizeStepTemplate(ShowMechanismSteps):
    CONFIG = dict(
        play_or_add="add",
        add_steps_one_by_one=True,
    )

    def construct(self):
        ShowMechanismSteps.construct(self);self.wait()
        self.fade_all_steps_except_index()

class EmphasizeStep0(EmphasizeStepTemplate):
    CONFIG = dict(
        unfaded_index=0
    )

class Step0(Scene):
    def construct(self):
        ## Bad idea, BAD IDEA!!
        # beaker = VGroup(
        #     Square().set_fill(BLUE,opacity=1).set_stroke(opacity=0),
        #     Line(DL,LEFT +1.5*UP),
        #     Line(DR,RIGHT+1.5*UP),
        #     Line(DL,DR)
        # ).shift(LEFT*2)

        # label=ChemObject("H_2 O").shift(2.8*UP/4).add_updater(lambda m: m.set_x_to_be_same_as_that_of(beaker))


        # self.play(Write(hydrogen_halide));self.wait()
        # self.play(ShowCreation(VGroup(beaker,label)));self.wait()
        # self.bring_to_front(hydrogen_halide)
        # self.play(ApplyMethod(hydrogen_halide.scale, 0.5),
        #           beaker.center,
        #           ApplyMethod(hydrogen_halide.move_to,2*UP,rate_func=there_and_back))
        # self.wait()

        hydrogen_halide = ChemObject("H-X",color=RED).scale(2)

        H = hydrogen_halide[0][0]
        Br= hydrogen_halide[0][1]
        bond = hydrogen_halide[0][2]

        hydrogen_halide[0][1].set_color(GREEN) ## Halide
        hydrogen_halide[0][2].set_color(YELLOW) ## Bond

        self.play(Write(hydrogen_halide))

        inductive_effect_arrows = InductiveArrows(num_arrows=3).move_to(hydrogen_halide[0][2]).set_color(BLUE)

        # self.play(Write(inductive_effect_arrows))


        H_elecs = Dot().match_color(H).next_to(H,RIGHT,buff=0.1)
        Br_elecs = VGroup(Dot().match_color(Br).next_to(Br,LEFT,buff=0.1),
            *[
                VGroup(
                    Dot().match_color(Br),
                    Dot().match_color(Br)
                ).arrange(rotate_vector(direction,PI/2),buff=0.2).next_to(Br,direction)

                for direction in [UP,RIGHT,DOWN]
            ]
        )

        footnote = TextMobject(
            "* Each ","green"," and ","red"," dot represents an ","electron",
            tex_to_color_map={
                "green":GREEN,"red":RED,"electron":YELLOW
            }
        ).scale(0.45).to_corner(DL)

        self.play(
            Write(VGroup(H_elecs,Br_elecs)),
            FadeIn(footnote)
        );self.wait(2)

        really_electro_pos = TextMobject("Really electropositive").shift(LEFT*2+DOWN).scale(0.75)
        really_electro_neg = TextMobject("Really electronegative").shift(RIGHT*2+DOWN).scale(0.75)

        # electropositive_indicator = Arrow(start=really_electro_pos.get_right(),end=H.get_left())
        # electronegative_indicator = Arrow(start=really_electro_neg.get_right(),end=Br.get_left())

        self.play(
            Write(VGroup(
                really_electro_pos,really_electro_neg
            ))
        );self.wait(2.5)

        self.play(inductive_effect_arrows.fade_in_one_by_one())
        self.wait(2)
        focus_rect = SurroundingRectangle(inductive_effect_arrows)
        inductive_effect_text = TextMobject("Inductive Effect").next_to(hydrogen_halide,UP,buff=1.5)
        self.play(
            ShowCreation(focus_rect),FadeInFrom(inductive_effect_text)
        );self.wait()


        partial_pos = TexMobject("\delta +").scale(0.75).next_to(focus_rect.points[0],UP,buff=0.15)
        partial_neg = TexMobject("\delta -").scale(0.75).next_to(focus_rect.points[3],UP,buff=0.15)

        # print(focus_rect.points)
        # for point in focus_rect.points:
        #     self.add(SmallDot(point))

        explanation_of_del_charge = TextMobject("``Partial'' charges").shift(UL+ LEFT).scale(0.6)
        expl_del_charge_arrow = Arrow(start=explanation_of_del_charge.get_corner(DR),end = partial_pos.get_corner(UL))

        self.play(Write(VGroup(partial_pos,partial_neg)));self.wait()

        self.play(
            Write(explanation_of_del_charge),
            ShowCreation(expl_del_charge_arrow)
        );self.wait(3)

        H_to_X = CurvedArrow(H.get_top(),Br.get_top()).flip(RIGHT).scale(0.75).shift(UP)
        self.play(ShowCreation(H_to_X))
        self.play(H_elecs.move_to,H_to_X.get_start())
        self.play(MoveAlongPath(H_elecs,H_to_X),
                  FadeOut(
                      VGroup(
                          partial_pos,
                          partial_neg,
                          explanation_of_del_charge,
                          expl_del_charge_arrow,
                          focus_rect,
                          inductive_effect_text,
                          bond
                        )
                    )
                );self.wait()

        self.play(
            H_elecs.next_to,Br_elecs[1],RIGHT,buff=3
        );self.wait()

        self.play(
            Transform(H_elecs,TexMobject("\\ominus",id="minus_indicator"),move_to=True),
            Write(TexMobject("\\oplus",id="plus_indicator").next_to(H.get_corner(UR),UR,buff=0.15)),
            FadeOut(H_to_X),
            FadeOut(VGroup(really_electro_pos,really_electro_neg))
        );self.wait(2)

        radicals = VGroup(
            ChemObject("\\charge{60:4pt=$\\oplus$}{H}").set_color(RED),
            ChemObject("\\charge{60:4pt=$\\ominus$}{X}").set_color(GREEN),
        ).arrange(RIGHT,buff=1).scale(2)


        self.play(
            ReplacementTransform(
                VGroup(
                    H,*[mob for mob in self.mobjects if mob.id=="plus_indicator"]
                ),
                radicals[0]
            ),
            ReplacementTransform(
                VGroup(
                    Br,*[mob for mob in self.mobjects if mob.id=="minus_indicator"],Br_elecs,H_elecs
                ),
                radicals[1]
            ),
            FadeOut(
                VGroup(hydrogen_halide[0][2],inductive_effect_arrows,footnote)
            )
        );self.wait(2)

        electrophile_text = BraceText(radicals[0],"Electrophile")
        self.play(electrophile_text.creation_anim());self.wait()
        # self.add(beaker,label,hydrogen_halide)
        # self.add(beaker)

class EmphasizeStep1(EmphasizeStepTemplate):
    CONFIG = {
        "unfaded_index":1
    }

class Step1(Scene):
    def construct(self):
        alkene = ChemWithName("CH_3-CH=CH_2","Prop-1-ene",id="alkene")

        self.play(alkene.creation_anim());self.wait(2)
        self.play(FadeOut(alkene.name))

        electrophile = ChemObject("\\charge{60:4pt=$\\oplus$}{H}").set_color(RED).to_corner(UR,buff=2.5)
        self.play(Write(electrophile));self.wait(2)

        self.play(
            Write(BondBreak(alkene[0][0][9],id="pi_bond_breaker"))
        )

        bond_electrons = ElectronPair().shift(UP*0.15)
        pi_bond = alkene[0][0][9]

        self.play(
            Unwrite(self.get_mobject_with_id("pi_bond_breaker")),
            ReplacementTransform(pi_bond,bond_electrons,move_to=True)
        );self.wait(2)

        # self.add(get_submobject_index_labels(alkene[0][0]))
        self.play(
            bond_electrons[0].next_to,alkene[0][0][3],DOWN,0.15,
            bond_electrons[1].next_to,alkene[0][0][6],DOWN,0.15
        );self.wait(2)

        option_1 = CurvedArrow(electrophile.get_bottom()+DOWN*0.20,bond_electrons[0].get_bottom(),angle=-TAU/3,buff=0.35)
        option_2 = CurvedArrow(electrophile.get_bottom()+DOWN*0.20,bond_electrons[1].get_bottom(),angle=-TAU/3,buff=0.35)

        self.play(
            GrowArrow(option_1)
        );self.wait()

        self.play(
            GrowArrow(option_2)
        );self.wait(5)

        self.set_variables_as_attrs(alkene,option_1,option_2,bond_electrons,electrophile)

class BetterCarbocations(Scene):
    def construct(self):
        one_degree=ChemObject("R-\\charge{90:4pt=$+$}{C}H_2")
        two_degree=ChemObject("R-\\charge{90:4pt=$+$}{C}H-R'")
        three_degree=ChemObject("R-\\charge{60:4pt=$+$}{C}(-[2]R')-R''")



        arranged_carbocations = VGroup(
            three_degree,
            two_degree,
            one_degree
        ).arrange(RIGHT,buff=2)

        three_degree.shift(UP*0.25)

        classifications = VGroup(
            *[TextMobject(f"{name} Degree").next_to(chem,DOWN)
            for name,chem in zip(("First","Second","Third"),(one_degree,two_degree,three_degree))
            ]
        )

        gt1 = TexMobject(">",id="gt1").shift(LEFT*2+DOWN*0.25)
        gt2 = TexMobject(">",id="gt2").shift(RIGHT*2.5+DOWN*0.25)

        self.play(
            LaggedStartMap(
                Write,arranged_carbocations
            ),
            LaggedStartMap(
                FadeInFrom,classifications
            )
        );self.wait()

        self.play(
            LaggedStartMap(
                Write,VGroup(gt1,gt2)
            )
        );self.wait()


        criteria = CArrow(text_up="Decreasing order of stability",length=4).shift(UP*2)

        self.play(
            FadeInFrom(criteria,LEFT)
        );self.wait(3)

class Path1(Step1):
    def construct(self):
        super().construct()

        self.option_2.set_opacity(0)

        # H_rad
        # print_family(self.alkene)
        self.wait()
        self.play(
            MoveAlongPath(
                self.electrophile,self.option_1,run_time=3,rate_func=smooth
            ),
            self.option_1.set_opacity,0
        );self.wait(2)
        print(self.foreground_mobjects)

        carbocation = ChemObject(
            "CH_3-CH(-[-2]H)-\\charge{90:4pt=$\\oplus$}{C}H_2"
        )

        #
        carbocation[0][6].set_color(RED) #Hydrogen
        carbocation[0][7].set_color_by_gradient(WHITE,WHITE,WHITE,RED) #Bond
        carbocation[0][9].set_color(GREEN) #Positive charge

        self.play(
            ReplacementTransform(
                VGroup(
                    *self.mobjects
                ),carbocation
            )
        );self.wait(2)

        braceWithLabel = BraceText(carbocation,"First Degree\\\\Carbocation")

        self.play(
            braceWithLabel.creation_anim()
        );self.wait(2)
        # self.add(get_submobject_index_labels(carbocation[0]))

class Path2(Step1):
    """This is basically a copy of Path1 with parameters changed. :P"""

    def construct(self):
        super().construct()

        self.option_1.set_opacity(0)

        self.wait()
        self.play(
            MoveAlongPath(
                self.electrophile,self.option_2,run_time=3,rate_func=smooth
            ),
            self.option_2.set_opacity,0
        );self.wait(2)
        # print(self.foreground_mobjects)

        carbocation = ChemObject(
            "CH_3-\\charge{90:4pt=$\\oplus$}{C}H-CH_2(-[-2]H)"
        )
        #
        carbocation[0][11].set_color(RED) #Hydrogen
        carbocation[0][12].set_color_by_gradient(WHITE,WHITE,WHITE,RED) #Bond
        carbocation[0][4].set_color(GREEN) #Positive charge

        self.play(
            ReplacementTransform(
                VGroup(
                    *self.mobjects
                ),carbocation
            )
        );self.wait(2)
        # self.add(get_submobject_index_labels(carbocation[0]))

        braceWithLabel = BraceText(carbocation,"Second Degree\\\\Carbocation")

        self.play(
            braceWithLabel.creation_anim()
        );self.wait(2)

class BetterCarbocationHere(Scene):
    def construct(self):
        first_degree = ChemObject(
            "CH_3-CH(-[-2]H)-\\charge{90:4pt=$\\oplus$}{C}H_2"
        ).shift(RIGHT*2.5)

        #
        first_degree[0][6].set_color(RED) #Hydrogen
        first_degree[0][7].set_color_by_gradient(WHITE,WHITE,WHITE,RED) #Bond
        first_degree[0][9].set_color(GREEN) #Positive charge

        second_degree = ChemObject(
            "CH_3-\\charge{90:4pt=$\\oplus$}{C}H-CH_2(-[-2]H)"
        )
        #
        second_degree[0][11].set_color(RED) #Hydrogen
        second_degree[0][12].set_color_by_gradient(WHITE,WHITE,WHITE,RED) #Bond
        second_degree[0][4].set_color(GREEN) #Positive charge

        braceWithLabelFirstDegree = BraceText(first_degree,"First Degree\\\\Carbocation").add_updater(
            lambda m: m.set_x_to_be_same_as_that_of(first_degree)
        )

        braceWithLabelSecondDegree = BraceText(second_degree,"Second Degree\\\\Carbocation").add_updater(
            lambda m: m.set_x_to_be_same_as_that_of(second_degree)
        )

        regioselectivity = TextMobject("Regioselectivity").to_edge(UP,buff=1.5).scale(2)

        self.add(second_degree,braceWithLabelSecondDegree)

        self.wait()

        self.play(
            second_degree.shift,LEFT*2.5,
            FadeIn(
                first_degree
            ),
            braceWithLabelFirstDegree.creation_anim()
        )

        self.play(
            FadeIn(
                TexMobject(">",stroke_width=2)
            )
        );self.wait()

        cancel = Cross(first_degree)

        self.play(Write(cancel));self.wait(2)

        self.play(FadeInFrom(regioselectivity))
        self.play(AnimationOnSurroundingRectangle(regioselectivity,rect_animation=ShowCreationThenDestruction),run_time=2.5)

        self.wait(3)

class InCaseOfTwoDoubleBonds(Scene):
    def construct(self):
        ddba = doublydoublebondedalkene = ChemObject("CH_2=CH-CH_2-CH=CH_2")
        symmetric_label = BraceText("Symmetric \\\\ alkene")
        self.play()

class DetourOnStabilityOfCarbocations(Scene):
    """Maybe make this a video of it's own instead?
    """
    def construct(self):
        one_degree=ChemObject("R-\\charge{90:4pt=$+$}{C}H_2")
        two_degree=ChemObject("R-\\charge{90:4pt=$+$}{C}H-R'")
        three_degree=ChemObject("R-\\charge{60:4pt=$+$}{C}(-[2]R')-R''")

        classifications = VGroup(
            *[TextMobject(f"{name} Degree").next_to(chem,DOWN)
            for name,chem in zip(("First","Second","Third"),(one_degree,two_degree,three_degree))
            ]
        )

        footnote = TextMobject("* Here, ","R,R' etc."," represent any hydrocarbon chain",tex_to_color_map={"R":RED})

        footnote.scale(0.5).to_corner()

        arranged_carbocations = VGroup(
            one_degree,
            two_degree,
            three_degree
        ).arrange(RIGHT,buff=2)

        three_degree.shift(UP*0.25)
        # self.add(get_submobject_index_labels(two_degree[0]))

        self.play(
            LaggedStartMap(
                Write,arranged_carbocations
            ),
            Write(footnote)
        );self.wait()




        # self.add(get_submobject_index_labels(one_degree[0]))

        # one_degree_inductive_effect_arrows = odiea = InductiveArrows(num_arrows=2,arrange_direction=RIGHT).move_to(one_degree[0][5])
        # odiea.set_color(BLUE)

        # self.play(
        #     Write(footnote),
        #     Write(
        #         one_degree
        #     )
        # );self.wait()

        # self.play(
        #     Unwrite(footnote),
        #     odiea.fade_in_one_by_one()
        # );self.wait()

        # self.play(
        #     FadeInFrom(classifications[0],UP)
        # );self.wait(2)

class EmphasizeStep2(EmphasizeStepTemplate):
    CONFIG = {
        "unfaded_index":2
    }

class Step2(Scene):
    def construct(self):
        carbocation = ChemObject(
            "CH_3-\\charge{90:4pt=$\\oplus$}{C}H-CH_2(-[-2]H)"
        )
        #
        carbocation[0][11].set_color(RED) #Hydrogen
        carbocation[0][12].set_color_by_gradient(WHITE,WHITE,WHITE,RED) #Bond
        carbocation[0][4].set_color(GREEN) #Positive charge


        nucleophile = ChemObject("\\charge{75:4pt=$\\ominus$}{Br}").set_color(BLUE).to_corner(UP+RIGHT,buff=1.75)

        self.add(carbocation)

        self.play(Write(nucleophile));self.wait()

        ghost_circle = Arc(
            start_angle=75*DEGREES,
            angle=195*DEGREES,
            radius=get_norm(nucleophile[0][2].get_center()-nucleophile[0][0].get_center())
        ).move_to(nucleophile[0][0])
        # self.add(get_submobject_index_labels(carbocation[0]))
        self.play(

            MoveAlongPath(nucleophile[0][2],ghost_circle),
        )
        self.play(
            ApplyMethod(nucleophile.next_to,carbocation[0][4],UP,dict(buff=0.3))
        )
        self.play(
            ApplyMethod(nucleophile.shift,LEFT*0.08)
        )

        show_electron_attack = CurvedArrow(nucleophile[0][2].get_left(),carbocation[0][4].get_left())
        show_electron_attack.tip.scale(0.5)

        self.play(ShowCreation(show_electron_attack));self.wait()

        bond = Line(nucleophile[0][2].get_bottom(),carbocation[0][4].get_top())

        self.play(Write(bond));self.wait()

        semi_final = ChemObject("CH_3-CH(-[2]Br)-CH_2(-[-2]H)")

        semi_final[0][6:8].set_color(BLUE)
        semi_final[0][3].set_color(GREEN)
        semi_final[0][13].set_color(RED)
        self.play(
            ReplacementTransform(
                VGroup(
                    *self.mobjects
                ),semi_final
            )
        );self.wait(2)

        label = BraceText(
            semi_final,"Product"
        )

        self.play(
            label.creation_anim()
        );self.wait(2)




        # self.add(get_submobject_index_labels(semi_final[0]))

class HistoryOfThisRule(Scene):
    def construct(self):
        markovnikov = ImageMobject("markovnikov").scale(2.5).shift(UP)
        markovnikov_details = TextMobject("Vladimir Vasilyevich Markovnikov \\\\ \small{(1838-1904)}").next_to(markovnikov,DOWN)

        kharasch = ImageMobject("kharasch").scale(2.5).shift(UP)
        kharasch_details = TextMobject("Morris Selig Kharasch \\\\ \small{(1895-1957)}").next_to(kharasch,DOWN)

        self.play(
            FadeIn(markovnikov)
        );self.wait()

        self.play(
            Write(markovnikov_details)
        );self.wait(6)


        self.play(
            Group(markovnikov,markovnikov_details).to_edge,LEFT,0.5,
            FadeIn(Group(kharasch,kharasch_details).to_edge(RIGHT,0.5))
        );self.wait(7)

class KharaschEffectTeaser(Scene):
    def construct(self):
        react = Reaction(
            ["CH_3-CH=CH_2"],
            ["CH_3-CH_2-CH_2-Br"],
            arrow_text_up="HBr/Peroxide",
            arrow_length=2
        )

        title = Title("Kharasch/Anti-Markovnikov Effect",tex_to_color_map={"Kharasch":RED,"Anti-Markovnikov":BLUE},include_underline=False)

        self.play(FadeInFrom(title));self.wait(2)
        self.play(
            Write(
                VGroup(
                    react[0],react[2]
                )
            ),
            FadeInFrom(react[1])
        );self.wait()


class TestScene(ThreeDScene):
    def construct(self):
        play_finish_sound()
class ReactionTest(Scene):
    def construct(self):
        # self.play(Write(SVGMobject("C:\\CodeProjects\\out_1.svg",stroke_width=0.5).scale(0.25)))

        react = Reaction(
            ["CH_3-CH_2-CH-LA"],
            ["CH_4"],
            arrow_text_up="HBr",
            arrow_length=2.5
        )
        print(react.tex_strings)
        # self.play(
        #     Write(
        #         VGroup(
        #             react[0:7],react[8:]
        #         )
        #     ),
        #     FadeInFrom(react[7])
        # );self.wait()
        self.play(Write(react));self.wait(2)
        # self.play(
        #     FadeInFrom(react[0:6])
        # );self.wait(2)
        # print_family(react)
        # self.add(get_submobject_index_labels(react[-1]))
        # self.play(Write(ChemArrow(length=4,text_up="AAAAAAAAA"),lag_ratio=0.75));self.wait()
        # self.wait(2)
        # breakpoint()

## Epic fail.
class Stretch(Transform):
    def create_target(self):
        return self.mobject

    def create_starting_mobject(self):
        return VGroup(*[submob.move_to(self.mobject.get_center()) for submob in self.mobject.submobjects])

class LogoScene(Scene):
    def construct(self):
        kilacoda = ChemWithName("K(-[1]I(-[::0]La(=[::90]Co(-[::-90]Da))))","KilaCoda")
        kilacoda.name.scale(1.75)
        kilacoda.chem.scale(1.5).shift(UP*0.5)

        ## Coloring
        for index in (0,1,3,4,6,7,10,11):
            kilacoda.chem[0][index].set_color(RED)

        self.play(kilacoda.creation_anim());self.wait(2)
        # self.add(get_submobject_index_labels(kilacoda.chem[0]))


class OutroScene(Scene):
    def construct(self):
        thanks = TextMobject("Thank you for watching!")
        copyright = TextMobject("All video content property of KilaCoda, i.e. Raghav Goel")

        thanks.scale(1.5).center()
        copyright.scale(0.5).to_corner(DOWN+LEFT).set_opacity(0.7)

        self.play(
            Write(thanks),
            # FadeIn(copyright)
        );self.wait(2)




class Thumbnail(Scene):
    def construct(self):
        example = Reaction(
            ["CH_2 = CH - CH_3"],
            ["CH_2(-[-2]H) - CH_2 (-[-2]Br) - CH_3"],
            arrow_text_up="\\chemfig{H-Br}",
            arrow_length=1.5
        )

        heading = Title("Markovnikov's Rule",include_underline=False).scale(3).center().shift(UP)
        heading.set_color_by_gradient(
                RED,YELLOW
                )

        self.add(heading,example.scale(0.75).shift(DOWN))




































## Just to make myself feel a little better by making something 1000 loc long lol.
