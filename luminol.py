from chanim import *
from pathlib import Path

LUMINOL = "*6(-=*6(-(=O)-N(-H)-N(-H)-(=O)--)-=(-NH_2)-=)"
DIANION_1 = "*6(-=*6(-(=O)-\\charge{45:2pt=$\\scriptstyle-$}{N}-\\charge{45:2pt=$\\scriptstyle-$}{N}-(=O)--)-=(-NH_2)-=)"
O2 = "O(=[-2]O)"


class ChemObjectTest(Scene):
    def construct(self):
        luminol = ChemObject("*6(-=*6(-(=O)-NH-NH-(=O)--)-=(-NH_2)-=)")
        self.play(Write(luminol))


class ChemReactionTest(Scene):
    def construct(self):
        react = Reaction(
            ["*6(-=*6(-(=O)-NH-NH-(=O)--)-=(-NH_2)-=)"],
            [
                "*6(-=*6(-(=O)-\\charge{45:2pt=$\\scriptstyle-$}{N}-\\charge{45:2pt=$\\scriptstyle-$}{N}-(=O)--)-=(-NH_2)-=)"
            ],
            arrow_type="eq",
        )
        self.play(react.show(reactant_product_simultaneity=True))


class LuminolIntro(Scene):
    def construct(self):
        word = Text("Chemiluminesence").scale(2).center()
        self.add(
            word,
            # get_submobject_index_labels(word)
        )

        brace1 = BraceText(word[0:5], "``chemical''", brace_direction=UP)
        brace2 = BraceText(word[5:], "``light''", brace_direction=DOWN)

        self.play(brace2.creation_anim(), Wait(), word[5:].set_color, BLUE)
        self.play(brace1.creation_anim(), Wait(), word[0:5].set_color, RED)
        self.wait(2)

        self.clear()

        self.show_examples()

        luminol = ChemWithName(
            LUMINOL,
            "Luminol\\\\\\footnotesize (5-Amino-2,3-dihydrophthalazine-1,4-dione)",
        ).shift(UP)
        self.play(luminol.creation_anim())
        self.wait(2)

        self.play(FadeOutAndShift(luminol.name), luminol.chem.shift, DOWN + 4 * LEFT)

        luminol_para = Paragraph(
            "Used in forensics", "to locate blood traces", "at crime scenes"
        ).to_edge(RIGHT)

        self.play(Write(luminol_para))
        self.wait()

    def show_examples(self):
        luciferin_bio_photo = ImageMobject(Path(".\\references\\firefly_glowing.jpg"))
        luceferin_text = Tex("Fireflies\\\\(luciferin)")
        luceferin_group = (
            Group(luciferin_bio_photo, luceferin_text).arrange(DOWN).to_edge(LEFT)
        )

        glow_stick_photo = ImageMobject(Path(".\\references\\glow_stick.jpg"))
        glow_stick_text = Tex("Glow sticks\\\\(Cyalume)")
        glow_stick_group = (
            Group(glow_stick_photo, glow_stick_text).arrange(DOWN).to_edge(RIGHT)
        )

        self.play(
            FadeInFrom(luceferin_group[0], UP),
            FadeInFrom(luceferin_group[1], DOWN),
        )

        self.wait()

        self.play(
            FadeInFrom(glow_stick_group[0], UP),
            FadeInFrom(glow_stick_group[1], DOWN),
        )

        self.wait()

        self.play(
            FadeOutAndShift(luceferin_group),
            FadeOutAndShift(glow_stick_group),
        )


class Synthesis(Scene):
    def setup(self):
        self.divider = Line(
            start=config["frame_y_radius"] * DOWN,
            end=config["frame_y_radius"] * UP,
        ).shift(RIGHT * 1.75)

        self.steps_header = (
            Text("Steps").next_to(self.divider).set_y(config["frame_y_radius"] - 1.5)
        )
        self.play(ShowCreation(self.divider), Write(self.steps_header))
        Transform

    def construct(self):
        self.steps = (
            BulletedList(
                "Heat 3-nitrophthalic\\\\acid with hydrazine\\\\in glycerol",
                "Reduce nitro group to\\\\amino group using\\\\sodium dithionite",
                tex_environment="flushleft",
            )
            .next_to(self.steps_header, DOWN, buff=1.25)
            .shift(1.75 * RIGHT)
        )
        self.play(Write(self.steps))

        self.play(
            self.steps.fade_all_but,
            0,
        )
        self.wait()

        ## Note: bond angles totally not accurate. required for demonstration and transtition purposes.
        npa = ChemObject(
            "*6(-=(-(=[-2]O)-[:30]O(-[-2]H))-(-(=[2]O)-[:-30]O(-[2]H))=(-NO_2)-=)"
        ).set_x(-1.5 * self.divider.get_x())

        self.play(Write(npa))

        hydrazine = (
            ChemObject("N(-[3]H)(-[-3]H)-N(-[1]H)(-[-1]H)")
            .move_to(npa)
            .shift(2 * RIGHT)
            .scale(0.85)
        )

        self.play(
            npa.shift,
            LEFT * 2,
            Write(hydrazine),
        )

        self.play(
            Rotate(hydrazine, angle=TAU / 4, run_time=0.5),
        )

        self.play(hydrazine.shift, LEFT)
        self.play(
            Rotate(hydrazine[0][0], -PI / 2),
            Rotate(hydrazine[0][1], -PI / 2),
            Rotate(hydrazine[0][3], -PI / 2),
            Rotate(hydrazine[0][5], -PI / 2),
            Rotate(hydrazine[0][7], -PI / 2),
            Rotate(hydrazine[0][9], -PI / 2),
            Transform(
                hydrazine[0][8], hydrazine[0][10].copy().scale(1.25).shift(LEFT * 1.25)
            ),
            Transform(
                hydrazine[0][2], hydrazine[0][4].copy().scale(1.25).shift(LEFT * 1.25)
            ),
        )
        self.wait(2)

        water_grp_1 = VGroup(
            npa[0][16],
            npa[0][18],
            npa[0][19],
            hydrazine[0][7],
            hydrazine[0][8],
        )

        water_grp_2 = VGroup(
            npa[0][7],
            npa[0][9],
            npa[0][10],
            hydrazine[0][1],
            hydrazine[0][2],
        )
        self.play(FadeOutAndShift(water_grp_1, UP), FadeOutAndShift(water_grp_2, DOWN))

        hydrazine = VGroup(
            hydrazine[0][0],
            hydrazine[0][3],
            hydrazine[0][4],
            hydrazine[0][5],
            hydrazine[0][6],
            hydrazine[0][9],
            hydrazine[0][10],
        )

        self.play(hydrazine.shift, LEFT * 1.5)

        self.wait()

        sodium_thiocyanide = ChemObject("Na_2 S_2 O_4")
        self.play(self.steps.fade_all_but, 1, Write(sodium_thiocyanide))

        footnote = (
            Tex(
                "* I'm not animating the reduction, just assume sodium thiocyanide is a reducing agent\\\\and it's reduced the nitro group",
                tex_environment="flushleft",
            )
            .scale(0.4)
            .to_corner()
        )

        self.play(npa[0][23].set_color, YELLOW)
        hydrogen = ChemObject("H").set_color(RED).move_to(npa[0][23])

        self.wait(2)
        self.play(
            FadeOutAndShift(npa[0][23], UP), FadeInFrom(hydrogen), Write(footnote)
        )
        self.wait()
        self.play(
            FadeOutAndShift(sodium_thiocyanide),
            FadeOutAndShift(footnote),
            hydrogen.set_color,
            WHITE,
        )
        luminol_created = VGroup(
            npa[0][0:7],
            npa[0][8],
            npa[0][11:16],
            npa[0][17],
            npa[0][20:23],
            npa[0][24:],
            hydrogen,
            hydrazine,
        )
        self.play(
            luminol_created.shift,
            RIGHT * 2,
        )

        luminol_label = Tex("Luminol").to_edge(DOWN).shift(2.5 * LEFT + UP * 0.5)

        self.play(Write(luminol_label))
        self.wait()
        self.play(
            Uncreate(self.divider),
            FadeOut(VGroup(self.steps,self.steps_header)),
            VGroup(luminol_created,luminol_label).center
        )
        self.add(
            get_submobject_index_labels(hydrazine[0]),
            get_submobject_index_labels(npa[0]),
        )


class LuminolReactionStyle1(Scene):
    def construct(self):
        luminol = ChemWithName(LUMINOL, "Luminol")
        hydroxide_1 = ChemObject("-OH").to_corner(UR, buff=1.5)
        hydroxide_2 = ChemObject("-OH").to_corner(DR, buff=1.5)

        self.play(luminol.creation_anim())
        self.wait()

        self.play(
            FadeInFrom(hydroxide_1, UP),
            FadeInFrom(hydroxide_2, DOWN),
        )

        self.play(
            ApplyMethod(
                hydroxide_1.next_to, luminol.chem[0][13], dict(buff=SMALL_BUFF)
            ),
            ApplyMethod(hydroxide_2.next_to, luminol.chem[0][9], dict(buff=SMALL_BUFF)),
        )

        water_group_1 = VGroup(luminol.chem[0][13], hydroxide_1)
        water_group_2 = VGroup(luminol.chem[0][9], hydroxide_2)

        self.play(
            Transform(water_group_1, ChemObject("H_2 O").move_to(water_group_1)),
            Transform(water_group_2, ChemObject("H_2 O").move_to(water_group_2)),
        )

        self.play(
            Transform(
                luminol.chem[0][14],
                MathTex("\\scriptstyle-").move_to(luminol.chem[0][14]),
            ),
            Transform(
                luminol.chem[0][10],
                MathTex("\\scriptstyle-").move_to(luminol.chem[0][10]).shift(UP * 0.5),
            ),
            FadeOutAndShift(luminol.name),
            FadeOutAndShift(water_group_1, UP),
            FadeOutAndShift(water_group_2, DOWN),
        )

        self.play(
            Transform(
                luminol.chem[0][14],
                luminol.chem[0][15].copy().scale(0.8).shift(DOWN * 0.1),
            ),
            Transform(
                luminol.chem[0][10],
                luminol.chem[0][8].copy().scale(0.8).shift(UP * 0.1),
            ),
            Transform(
                luminol.chem[0][18],
                MathTex("\\scriptstyle-").next_to(
                    luminol.chem[0][16], UR + UP, buff=0.1
                ),
            ),
            Transform(
                luminol.chem[0][5],
                MathTex("\\scriptstyle-").next_to(
                    luminol.chem[0][4], UR + UP, buff=0.1
                ),
            ),
            luminol.chem[0][17].shift,
            0.05 * RIGHT,
            luminol.chem[0][6].shift,
            0.05 * RIGHT,
            # luminol.chem[0][14].next_to,luminol.chem[0][15],DL,dict(buff=0.15)
        )

        o2 = ChemObject(O2).to_edge(RIGHT, buff=2)

        self.play(Write(o2))

        self.play(
            MoveAlongPath(
                o2[0][2],
                ArcBetweenPoints(
                    o2[0][2].get_center(), o2[0][2].get_center() + UP + 0.05 * LEFT
                ),
            ),
            o2[0][3].shift,
            RIGHT * 0.05,
        )

        self.play(
            o2.scale,
            0.75,
            o2.next_to,
            luminol.chem[0][16],
            DOWN,
            {"buff": 0.8},
            Transform(
                luminol.chem[0][14],
                luminol.chem[0][12].copy().shift(0.1 * LEFT),
            ),
            Transform(
                luminol.chem[0][10],
                ## NOTE: This is totally not a weird workaround...
                o2[0][3].copy().next_to(luminol.chem[0][4], UP, buff=0.85),
            ),
        )

        self.play(
            Transform(
                luminol.chem[0][8],
                luminol.chem[0][12].copy().shift(0.1 * RIGHT),
            ),
            Transform(
                o2[0][3],
                MathTex("\\scriptstyle-").move_to(o2[0][1]).shift(UR * 0.25),
            ),
            Transform(
                luminol.chem[0][15],
                MathTex("\\scriptstyle-").move_to(o2[0][0]).shift(UR * 0.25),
            ),
            Transform(
                luminol.chem[0][5], luminol.chem[0][6].copy().shift(0.05 * RIGHT)
            ),
            Transform(
                luminol.chem[0][18], luminol.chem[0][17].copy().shift(0.05 * RIGHT)
            ),
            luminol.chem[0][6].shift,
            0.05 * LEFT,
            luminol.chem[0][17].shift,
            0.05 * LEFT,
        )

        n2 = VGroup(
            luminol.chem[0][7],
            luminol.chem[0][8],
            luminol.chem[0][11],
            luminol.chem[0][12],
            luminol.chem[0][14],
        )

        ## Updaters because rotating multiple things simultaneously in manim can be a PITA at times.
        o2[0][0].add_updater(lambda m: m.next_to(o2[0][2].get_end(), DOWN, buff=0.1))
        luminol.chem[0][15].add_updater(lambda m: m.move_to(o2[0][0]).shift(UR * 0.25))

        o2[0][1].add_updater(
            lambda m: m.next_to(o2[0][0], DOWN, buff=0.3)
        )  ## because when you can't update up, you gotta look down.
        o2[0][3].add_updater(lambda m: m.move_to(o2[0][1]).shift(UR * 0.25))
        self.play(
            n2.shift,
            3 * RIGHT,
            Transform(
                o2[0][2], luminol.chem[0][0].copy().shift(RIGHT * 2.55 + UP * 1.5)
            ),
            Transform(
                luminol.chem[0][10],
                luminol.chem[0][28].copy().shift(RIGHT * 2.55 + DOWN * 1.5),
            ),
        )

        three_APA = ChemWithName(
            ComplexChemIon(
                "*6(-=(-(=[-2]O)-[:36]\\charge{45:2pt=$\\scriptstyle-$}{O})-(-(=[2]O)-[:-36]\\charge{45:2pt=$\\scriptstyle-$}{O})=(-NH_2)-=)",
                charge="*",
            ).scale(0.75),
            "3-Aminophthalamine* (3-APA*)",
        )

        three_APA.chem[0][45:].shift(RIGHT * 0.2)
        o2[0][0].clear_updaters()
        o2[0][1].clear_updaters()
        o2[0][3].clear_updaters()
        luminol.chem[0][15].clear_updaters()

        self.play(
            ReplacementTransform(
                VGroup(
                    ## Yeah, yeah I know I should be using a slice here and not individual elements like a caveman.
                    ## Except the previous times I've tried to be lazy and do that the results were less than stellar.
                    luminol.chem[0][0],
                    luminol.chem[0][1],
                    luminol.chem[0][2],
                    luminol.chem[0][3],
                    luminol.chem[0][4],
                    luminol.chem[0][5],
                    luminol.chem[0][6],
                    luminol.chem[0][10],
                    luminol.chem[0][15],
                    luminol.chem[0][16],
                    luminol.chem[0][17],
                    luminol.chem[0][18],
                    luminol.chem[0][19],
                    luminol.chem[0][20],
                    luminol.chem[0][21],
                    luminol.chem[0][22],
                    luminol.chem[0][23],
                    luminol.chem[0][24],
                    luminol.chem[0][25],
                    luminol.chem[0][26],
                    luminol.chem[0][27],
                    luminol.chem[0][28],
                    luminol.chem[0][29],
                    luminol.chem[0][30],
                    o2[0][0],
                    o2[0][1],
                    o2[0][2],
                    o2[0][3],
                ),
                three_APA.chem,
            ),
            FadeInFrom(three_APA.name),
        )
        light = Tex("h$\\nu$").center().shift(RIGHT * 1.5)
        light_boundary = AnimatedBoundary(
            light, colors=[BLUE_A, BLUE_B, BLUE_C, BLUE_D], cycle_rate=2
        )
        self.wait()
        self.play(
            FadeOutAndShiftDown(
                VGroup(
                    three_APA.chem[0][0:18], three_APA.chem[0][45:63], three_APA.name
                )
            ),
            three_APA.chem[0][18:45].shift,
            LEFT * 2.5,
            ReplacementTransform(three_APA.chem[0][63], light),
        )
        self.add(light_boundary)
        self.wait(3)
        self.play(
            # FadeOutAndShift(VGroup(three_APA.chem[0][18:45], n2)),
            # ApplyFunction(lambda m: m.scale(2.5).shift(LEFT * 4), light),
            ApplyFunction(
                lambda m: m.scale(0.6).shift(LEFT * 3),
                VGroup(three_APA.chem[0][18:45], n2, light),
            ),
        )

        self.play(
            Write(
                DashedLine(
                    start=config["frame_y_radius"] * DOWN,
                    end=config["frame_y_radius"] * UP,
                ).next_to(n2,buff=1).set_opacity(0.65),
                run_time=0.5
            ),
            FadeInFrom(
                ImageMobject(Path(".\References_and_Movies\luminol_light.jpg"))
                .next_to(light, buff=2)
                .scale(0.8)
            ),
        )
        self.wait(3)

        # self.add(get_submobject_index_labels(three_APA.chem[0]))
        # self.add(get_submobject_index_labels(o2[0]))

        # self.add(get_submobject_index_labels(luminol.chem[0]))


class AminoPhthalate(Scene):
    def construct(self):
        three_APA = ChemObject(
            "*6(-=(-(=[-2]O)-[:36]\\charge{45:2pt=$\\scriptstyle-$}{O})-(-(=[2]O)-[:-36]\\charge{45:2pt=$\\scriptstyle-$}{O})=-=)"
        )

        self.add(three_APA, get_submobject_index_labels(three_APA[0]))
