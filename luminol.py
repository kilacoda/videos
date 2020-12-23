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
