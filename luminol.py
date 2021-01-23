from chanim import *
from pathlib import Path

LUMINOL = "*6(-=*6(-(=O)-N(-H)-N(-H)-(=O)--)-=(-NH_2)-=)"
DIANION_1 = "*6(-=*6(-(=O)-\\charge{45:2pt=$\\scriptstyle-$}{N}-\\charge{45:2pt=$\\scriptstyle-$}{N}-(=O)--)-=(-NH_2)-=)"
O2 = "O(=[-2]O)"
endoperoxide = None

config["tex_template"] = TexTemplateLibrary.simple

## Custom Mobjects ##
class JablonskiDiagram(VGroup):
    def __init__(self, label, num_vibs, **kwargs):
        self.ground_state = Line(stroke_width=3)
        self.vibs = VGroup(*[Line(stroke_width=0.5) for i in range(num_vibs)]).arrange(
            UP
        )

        super().__init__(self.ground_state, self.vibs, **kwargs)

        self.arrange(UP)
        self.label = MathTex(label).next_to(self.ground_state, LEFT)
        self.add(self.label)


class WigglyArrow(TipableVMobject):
    def __init__(
        self,
        num_wiggles=4,
        amplitude=0.5,
        wiggle_radius=0.5,
        final_line_length=0.5,
        **kwargs,
    ):
        self.num_wiggles = num_wiggles
        self.amplitude = amplitude
        self.wiggle_radius = wiggle_radius
        self.final_line_length = final_line_length

        super().__init__(**kwargs)
        self.add_tip()

    def generate_points(self):
        new_points = [
            ((-1) ** (x // 2)) * self.amplitude * UP + self.wiggle_radius * x * RIGHT
            if (x % 2 != 0)
            else ORIGIN
            if x == 0
            else self.wiggle_radius * x * RIGHT
            for x in range(2 * self.num_wiggles + 1)
        ]
        self.set_points_smoothly(new_points)
        final_point = new_points[-1] + self.final_line_length * RIGHT
        self.add_line_to(final_point)
        self.center()


## Scenes ##
class MechanismScene(Scene):
    def setup(self):
        self.divider = Line(
            start=config["frame_y_radius"] * DOWN,
            end=config["frame_y_radius"] * UP,
        ).shift(RIGHT * 1.75)

        self.steps_header = (
            Text("Steps").next_to(self.divider).set_y(config["frame_y_radius"] - 1.5)
        )
        self.play(ShowCreation(self.divider), Write(self.steps_header))

    def add_steps(
        self,
        *steps,
        animation=Write,
        buff_factor=0.25,
        scale_factor=0.8,
        extra_methods: str = None,
        animate=True,
        **bulleted_list_kwargs,
    ):
        self.steps = (
            BulletedList(*steps, **bulleted_list_kwargs)
            .next_to(self.steps_header, DOWN, buff=buff_factor)
            .shift(1.75 * RIGHT)
            .scale(scale_factor)
        )

        ## This could be pretty handy.
        exec(f"self.steps.{extra_methods}")

        if animate:
            self.play(animation(self.steps))
        else:
            self.add(self.steps)


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

        self.play(brace2.creation_anim(), Wait(), word[5:].animate.set_color(BLUE))
        self.play(brace1.creation_anim(), Wait(), word[0:5].animate.set_color(RED))
        self.wait(2)

        self.clear()

        self.show_examples()

        luminol = ChemWithName(
            LUMINOL,
            "Luminol\\\\\\footnotesize (5-Amino-2,3-dihydrophthalazine-1,4-dione)",
        ).shift(UP)
        self.play(luminol.creation_anim())
        self.wait(2)

        self.play(
            FadeOutAndShift(luminol.name), luminol.chem.animate.shift(DOWN + 4 * LEFT)
        )

        # luminol_para = Paragraph(
        #     "Used in forensics", "to locate blood traces", "at crime scenes"
        # ).to_edge(RIGHT)

        luminol_profile = MoleculeProfile(
            "Luminol", "3-aminophthalazide", "Forensics, Biology", 1902
        )
        self.play(luminol_profile.creation_anim())
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


## NOTE: Write doesn't seem to work with this. Use creation_anim instead.
class MoleculeProfile(VGroup):
    def __init__(
        self, name: str, iupac_name: str, uses: str, first_synthesis: int, **kwargs
    ):
        self.name = name
        self.iupac_name = iupac_name
        self.uses = uses
        self.first_synthesis = first_synthesis

        self.title = Text("Molecule Profile").add_background_rectangle(
            opacity=1
        )  # heh heh, they'll never know...
        dummy_underline = Underline(self.title)

        self.divider = Line(
            # dummy_underline.get_center(),
            # dummy_underline.get_center()
            # + (dummy_underline.get_y() + config["frame_y_radius"]) * DOWN,
            config["frame_y_radius"] * UP * 0.6,
            config["frame_y_radius"] * DOWN * 0.6,
        )

        # self.fields = (
        #     VGroup(
        #         Tex("Name"),
        #         Tex("IUPAC Name"),
        #         Tex("Used in"),
        #         Tex("First synthesis"),
        #     )
        #     .arrange(DOWN, buff=1)
        #     .align_to(UP)
        # )

        self.fields = Paragraph(
            "Name\n\n",
            # "IUPAC Name\n",
            "Used in\n",
            "First synthesis\n",
            line_spacing=2,
            size=0.65,
            font="Syne",
        )

        self.values = Paragraph(
            self.name,
            f"({self.iupac_name})" + "\n",
            self.uses + "\n",
            str(self.first_synthesis) + "\n",
            # line_spacing = 100, yup this is broken ig
            size=0.65,
        )
        # self.values = (
        #     VGroup(
        #         Tex(self.name),
        #         Tex(self.iupac_name),
        #         Tex(self.uses),
        #         Tex(str(self.first_synthesis)),
        #     )
        #     .arrange(DOWN, buff=1)
        #     .align_on_border(UP)
        # )

        bounding_lines = VGroup(Line())
        real_underline = Line(2 * LEFT, 2 * RIGHT)
        content = (
            VGroup(
                self.fields,
                self.divider,
                self.values
                # VGroup(self.fields, self.values).arrange(buff=1)
            )
            .arrange()
            .center()
        )
        super().__init__(
            self.title,
            # real_underline,
            content,
            **kwargs,
        )
        # self.divider.shift(DOWN)

        self.arrange(DOWN, buff=0.25)

        content.shift(RIGHT)
        self.to_edge(RIGHT)
        self.title.shift(RIGHT / 2)

        self.add_underline()

    def add_underline(self):
        self.underline = underline = Underline(self.title, buff=MED_SMALL_BUFF)
        self.add(underline)

    def creation_anim(self):
        title_anim = FadeIn(self.title)
        field_anims = [FadeInFrom(line) for line in self.fields.chars]
        value_anims = [FadeInFrom(line) for line in self.values.chars]
        divider_anim = FadeIn(self.divider)
        underline_anim = DrawBorderThenFill(self.underline)
        console.print("Hi! From line 281")
        return AnimationGroup(
            title_anim,
            divider_anim,
            underline_anim,
            *field_anims,
            *value_anims,
        )


class MoleculeProfileTest(Scene):
    def construct(self):
        profile = MoleculeProfile(
            "Luminol", "3-aminophthalazide", "Forensics, biology", 1938
        )

        self.play(profile.creation_anim())

        self.wait()


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
            self.steps.animate.fade_all_but(0),
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
            npa.animate.shift(LEFT * 2),
            Write(hydrazine),
        )

        self.play(
            Rotate(hydrazine, angle=TAU / 4, run_time=0.5),
        )

        self.play(hydrazine.animate.shift(LEFT))
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

        self.play(hydrazine.animate.shift(LEFT * 1.5))

        self.wait()

        sodium_thiocyanide = ChemObject("Na_2 S_2 O_4")
        self.play(self.steps.animate.fade_all_but(1), Write(sodium_thiocyanide))

        footnote = (
            Tex(
                "* I'm not animating the reduction, just assume sodium thiocyanide is a reducing agent\\\\and it's reduced the nitro group",
                tex_environment="flushleft",
            )
            .scale(0.4)
            .to_corner()
        )

        self.play(npa[0][23].animate.set_color(YELLOW))
        hydrogen = ChemObject("H").set_color(RED).move_to(npa[0][23])

        self.wait(2)
        self.play(
            FadeOutAndShift(npa[0][23], UP), FadeInFrom(hydrogen), Write(footnote)
        )
        self.wait()
        self.play(
            FadeOutAndShift(sodium_thiocyanide),
            FadeOutAndShift(footnote),
            hydrogen.animate.set_color(WHITE),
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
            luminol_created.animate.shift(RIGHT * 2),
        )

        luminol_label = Tex("Luminol").to_edge(DOWN).shift(2.5 * LEFT + UP * 0.5)

        self.play(Write(luminol_label))
        self.wait()
        self.play(
            Uncreate(self.divider),
            FadeOut(VGroup(self.steps, self.steps_header)),
            VGroup(luminol_created, luminol_label).center,
        )
        self.add(
            get_submobject_index_labels(hydrazine[0]),
            get_submobject_index_labels(npa[0]),
        )


class LuminolReactionMechanism(MechanismScene):
    steps_list = [
        "Deprotonation (removal\\\\of hydrogen) and\\\\dianion formation",
        "Rearrangement of charges\\\\(tautomerisation)",
        "Liberation of $\\text{N}_2$\\\\and formation of\\\\unstable 3-APA (3-APA*)",
        "Release of photon\\\\emitting blue light",
    ]

    def construct(self):
        global endoperoxide  # needed for reasoning scene

        self.add_steps(
            *self.steps_list,
            extra_methods="shift(UP*0.65)",
        )

        luminol = ChemWithName(LUMINOL, "Luminol").shift(LEFT * 3)
        hydroxide_1 = ChemObject("-OH").next_to(self.steps_header, LEFT, buff=0.75)
        hydroxide_2 = ChemObject("-OH").next_to(hydroxide_1, DOWN, buff=4.5)

        self.play(luminol.creation_anim())
        self.wait()

        ## Step 1 start
        self.play(self.steps.animate.fade_all_but(0))
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
        ## Step 1 end

        self.wait(2)

        ## Step 2 start
        self.play(self.steps.animate.fade_all_but(1))

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
            luminol.chem[0][17].animate.shift(0.05 * RIGHT),
            luminol.chem[0][6].animate.shift(0.05 * RIGHT),
            # luminol.chem[0][14].next_to,luminol.chem[0][15],DL,dict(buff=0.15)
        )
        ## Step 2 end

        ## Step 3 start
        self.play(self.steps.animate.fade_all_but(2))

        o2 = ChemObject(O2).next_to(luminol.chem, buff=0.75)
        o2.scale(0.75)

        self.play(Write(o2))

        self.play(
            MoveAlongPath(
                o2[0][2],
                ArcBetweenPoints(
                    o2[0][2].get_center(),
                    o2[0][2].get_center() + UP * 0.75 + 0.05 * LEFT,
                ),
            ),
            o2[0][3].animate.shift(RIGHT * 0.05),
        )

        self.play(
            o2.animate.next_to(luminol.chem[0][16], DOWN, buff=0.8),
            Transform(
                luminol.chem[0][14],
                luminol.chem[0][12].copy().shift(0.1 * LEFT),
            ),
            Transform(
                luminol.chem[0][10],
                ## This is totally not a weird workaround...
                o2[0][3].copy().scale(1.5).next_to(luminol.chem[0][4], UP, buff=0.85),
            ),
        )

        # self.add(
        #     get_submobject_index_labels(luminol.chem[0]).set_color(BLUE),
        #     get_submobject_index_labels(o2[0]).set_color(RED),
        # )

        ## To be used in ReasonsBehindChemiluminescence
        endoperoxide = VGroup(
            luminol.chem[0][0:9].copy(),
            luminol.chem[0][10:13].copy(),
            luminol.chem[0][14:].copy(),
            o2[0][:].copy(),
        )

        self.wait()

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
            luminol.chem[0][6].animate.shift(0.05 * LEFT),
            luminol.chem[0][17].animate.shift(0.05 * LEFT),
        )

        self.wait(2.5)
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
            n2.animate.shift(2 * RIGHT),
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
        ).shift(LEFT * 4.5)
        three_APA.name.scale(0.75).shift(UP * 0.5)

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
        ## Step 3 end

        ## Step 4 start
        self.play(self.steps.animate.fade_all_but(3))

        light = Tex("h$\\nu$").center().shift(LEFT * 1.5)
        light_boundary = AnimatedBoundary(
            light, colors=[BLUE_A, BLUE_B, BLUE_C, BLUE_D], cycle_rate=2
        )
        self.wait()
        self.play(
            FadeOutAndShift(
                VGroup(
                    three_APA.chem[0][0:18], three_APA.chem[0][45:63], three_APA.name
                )
            ),
            # three_APA.chem[0][18:45].animate.shift(LEFT * 2.5),
            ReplacementTransform(three_APA.chem[0][63], light),
        )
        self.add(light_boundary)
        self.wait(3)
        # self.play(
        #     # FadeOutAndShift(VGroup(three_APA.chem[0][18:45], n2)),
        #     # ApplyFunction(lambda m: m.scale(2.5).shift(LEFT * 4), light),
        #     ApplyFunction(
        #         lambda m: m.scale(0.6).shift(LEFT * 3),
        #         VGroup(three_APA.chem[0][18:45], n2, light),
        #     ),
        # )

        self.play(
            # Write(
            #     DashedLine(
            #         start=config["frame_y_radius"] * DOWN,
            #         end=config["frame_y_radius"] * UP,
            #     )
            #     .next_to(n2, buff=1)
            #     .set_opacity(0.65),
            #     run_time=0.5,
            # ),
            FadeInFrom(
                ImageMobject(Path(".\\references\luminol_light.jpg"))
                .to_edge(RIGHT)
                .shift(RIGHT)
                # .next_to(light, buff=2)
                # .scale(0.8)
            ),
        )
        self.wait(5)
        ## Step 4 end
        self.clear()
        ## Debug Stuff
        # self.add(get_submobject_index_labels(three_APA.chem[0]))
        # self.add(get_submobject_index_labels(o2[0]))

        # self.add(get_submobject_index_labels(luminol.chem[0]))


class EnergyDiagramIntermission(Scene):
    def construct(self):
        title = Title("Jablonski Diagram", include_underline=True).shift(UP * 0.2)

        self.play(Write(title))

        s0, s1, t1 = self.get_jablonski_diagrams()

        t1.label.next_to(t1.ground_state, RIGHT)

        VGroup(s0, s1).arrange(UP, buff=2).shift(LEFT * 2)

        t1.next_to(s1, 2 * RIGHT + DOWN * 0.5, buff=1).shift(UP * 1.5)

        # self.add(s0, s1, t1)

        trend_arrow = (
            VGroup(Tex("Energy"), Arrow(start=2 * DOWN, end=2 * UP))
            .arrange()
            .to_edge(buff=1)
        )

        self.play(
            Write(
                VGroup(
                    trend_arrow[0],
                    s0,
                    s1,
                    t1,
                )
            ),
            FadeInFrom(trend_arrow[1]),
        )

        vibrational_states_brace = BraceText(
            s0.vibs, "Vibrational\\\\states", brace_direction=RIGHT
        )
        self.play(vibrational_states_brace.creation_anim())
        self.play(FadeOut(vibrational_states_brace))

        explanations = VGroup(
            Text("(More excited\nsinglet state)")
            .next_to(s1.ground_state, DOWN, buff=0)
            .scale(0.5),
            Text("(Unstable\ntriplet state)")
            .next_to(t1.ground_state, DOWN, buff=0)
            .scale(0.5),
            Text("(Less excited\nsinglet state)")
            .next_to(s0.ground_state, DOWN)
            .scale(0.5),
        )

        self.play(ShowCreation(explanations))
        self.wait()
        self.play(Uncreate(explanations))

        electron = MathTex("\\upharpoonleft").scale(2)

        electron.move_to(t1.vibs[1]).set_color(RED)

        self.play(Write(electron))

        self.wait()

        intersystem_crossing_arrow = WigglyArrow(10, 0.25, 0.15).put_start_and_end_on(
            t1.ground_state.get_start(), s1.ground_state.get_end()
        )

        intersystem_crossing_label = BraceText(
            intersystem_crossing_arrow, "Intersystem Crossing"
        )

        def update_rotate_and_shift(mob: Mobject):
            # Rotate(mob)
            mob.move_to(s1.vibs[1]).rotate(PI).flip()  ## ehh, good enough
            return mob

        self.play(
            ShowCreation(intersystem_crossing_arrow),
            intersystem_crossing_label.creation_anim(),
        )

        self.wait()
        self.play(FadeOutAndShift(intersystem_crossing_label))

        self.play(
            # Rotate(electron),
            # ApplyFunction(update_rotate_and_shift, electron)
            electron.animate.move_to(s1.vibs[1])
            .rotate(PI)
            .flip()
        )
        self.play(
            electron.animate.move_to(s1.vibs[1]),
        )

        arrow_info_1 = (
            VGroup(
                Arrow(RIGHT, LEFT),
                Text(
                    "More stable as\nmolecule is less\nreactive due to\nall orbitals being filled"
                ).scale(0.5),
            )
            .arrange()
            .next_to(s1.vibs[1])
        )

        self.play(
            FadeIn(arrow_info_1),
            Wait(2),
        )

        photon = Circle(BLUE, fill_opacity=0.8).scale(0.5)
        photon.add(Tex("h$\\nu$").add_updater(lambda m, dt: m.move_to(photon)))

        photon.next_to(s1.ground_state, DOWN * 1.5)

        def some_updater(m: Mobject, dt):
            m.shift(dt * (3 * RIGHT + 1 * DOWN))
            # FadeIn(m)
            return m

        photon.add_updater(some_updater)

        write_and_shift_photon = AnimationGroup(
            Write(photon), ApplyMethod(photon.shift, 3 * RIGHT + 2 * DOWN)
        )
        # self.add(photon)
        self.play(
            electron.animate.move_to(s0.vibs[1]),
            # arrow_info_1.next_to,s0.vibs[1],dict(buff=0.5),
            FadeOut(arrow_info_1),
            Show(photon),
            # ApplyFunction(some_updater,photon)
            # photon.shift,
            # 3 * RIGHT + 2 * DOWN,
            # FadeIn(photon),
            # write_and_shift_photon
        )
        self.wait(2)

    def get_jablonski_diagrams(self):
        return [JablonskiDiagram(label, 5) for label in ["S_{0}", "S_{1}", "T_{1}"]]


class SomeDefinitions(Scene):
    def construct(self):
        head = Text("PAUSE for basic definitions").to_edge(UP, buff=1.5)
        definitions = BulletedList(
            "Triplet State - A molecule is said to be in a triplet state\\\\if there's at least one unpaired electron\\\\in its orbitals.",
            "Singlet State - And a singlet state is one in which\\\\there're no unpaired electrons in its orbitals.",
        ).center()

        self.add(head, definitions)
        self.wait()


class Show(Write):
    """
    Show a Mobject without animation.
    """

    def get_bounds(self, alpha):
        if alpha > 0:
            alpha = 1
        return (0, alpha)


class SynthesisVideoSuggestion(Scene):
    def construct(self):
        nilered_box, nurdrage_box = Rectangle(height=3, width=4), Rectangle(
            height=3, width=4
        )
        nilered_text, nurdrage_text = Tex("NileRed"), Tex("NurdRage")

        VGroup(
            VGroup(nilered_box, nilered_text).arrange(DOWN, buff=0.5),
            VGroup(nurdrage_box, nurdrage_text).arrange(DOWN, buff=0.5),
        ).arrange(RIGHT, buff=1.5)

        self.play(
            Write(nurdrage_text),
            Write(nilered_text),
            ShowCreation(nurdrage_box),
            ShowCreation(nilered_box),
        )
        self.wait(2)


class LuminolInstagram(Scene):
    def construct(self):
        watermark = (
            Tex("Follow @kilacoda for more")
            .to_corner(LEFT + DOWN)
            .set_opacity(0.5)
            .scale(0.75)
        )
        self.add(watermark)

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
            luminol.chem[0][17].animate.shift(0.05 * RIGHT),
            luminol.chem[0][6].animate.shift(0.05 * RIGHT),
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
            o2[0][3].animate.shift(RIGHT * 0.05),
        )

        self.play(
            o2.animate.scale(0.75).next_to(luminol.chem[0][16], DOWN, buff=0.8),
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
            luminol.chem[0][6].animate.shift(0.05 * LEFT),
            luminol.chem[0][17].animate.shift(0.05 * LEFT),
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
            n2.animate.shift(3 * RIGHT),
            # {"run_time":2},
            Transform(
                o2[0][2], luminol.chem[0][0].copy().shift(RIGHT * 2.55 + UP * 1.5)
            ),
            Transform(
                luminol.chem[0][10],
                luminol.chem[0][28].copy().shift(RIGHT * 2.55 + DOWN * 1.5),
            ),
            run_time=2,
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
            FadeOutAndShift(
                VGroup(
                    three_APA.chem[0][0:18], three_APA.chem[0][45:63], three_APA.name
                )
            ),
            three_APA.chem[0][18:45].animate.shift(LEFT * 2.5),
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
                )
                .next_to(n2, buff=1)
                .set_opacity(0.65),
                run_time=0.5,
            ),
            FadeInFrom(
                ImageMobject(Path(".\\references\luminol_light.jpg"))
                .next_to(light, buff=2)
                .scale(0.8)
            ),
        )
        self.wait(3)

        self.clear()

        self.add(
            Text(
                "Made with chanim\nhttps://github.com/raghavg123/chanim\n\nSource code at https://github.com/kilacoda/videos"
            ).scale(0.75)
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


class ImNotAChemistYaKnow(Scene):
    def construct(self):
        self.wait(2)
        self.add(Text("¯\_(ツ)_/¯"))

        self.wait()
        self.clear()
        self.wait(2)


class DisclaimerMechanismComplexAndABitUnknown(Scene):
    def construct(self):
        head = Text("Disclaimer", weight=BOLD).center().shift(UP * 2).scale(2)

        disc = Paragraph(
            "The mechanism explained here",
            "is the most commonly accepted proposal",
            "and the complete mechanism of the",
            "reaction is still a matter of debate.",
        ).next_to(head, DOWN * 4)
        self.play(Write(head), FadeIn(disc), run_time=3)
        self.wait()


class ReasonsBehindChemiluminescence(LuminolReactionMechanism):
    ##NOTE: Start render from 27th anim i.e. with `-n 27`
    def construct(self):
        super().construct()
        self.clear()
        self.setup()
        self.add_steps(
            *super().steps_list,
            extra_methods="shift(UP*0.65)",
        )

        self.play(
            self.steps.animate.fade_all_but(2),
            AnimationGroup(*[Write(part) for part in endoperoxide]),
        )
        # self.add(
        #     get_submobject_index_labels(endoperoxide[0]).set_color(RED),
        #     get_submobject_index_labels(endoperoxide[1]).set_color(BLUE),
        #     get_submobject_index_labels(endoperoxide[2]).set_color(GREEN),
        #     get_submobject_index_labels(endoperoxide[3]).set_color(YELLOW),
        # )

        self.endoperoxide_label = endoperoxide_label = Tex("Endoperoxide").next_to(
            endoperoxide, DOWN * 2
        )

        self.play(
            FadeInFrom(endoperoxide_label),
        )

        # console.print(endoperoxide[3][3].get_bottom()-endoperoxide[3][1].get_center())
        # console.print(endoperoxide[3][3].get_start(),endoperoxide[3][3].get_end())
        # self.wait()

        self.show_stretching()

        self.wait()

        self.electroncloud = ElectronCloud(endoperoxide[3][0])
        # self.play(FadeIn(electroncloud))
        self.wait()

    def show_stretching(self):
        endoperoxide.save_state()

        self.add_endoperoxide_updaters()
        # console.print(endoperoxide[1][0].get_top(),endoperoxide[1][0].get_bottom())
        # console.print(
        #     endoperoxide[1][0].points,
        #     endoperoxide[3][1].points,
        #     endoperoxide[3][3].points,
        # )

        # bond_length_decrementer = ValueTracker(1)

        # def C_O_bond_updater(m: VMobject):
        #     m.next_to(endoperoxide[0][6], UP, buff=0).stretch(
        #         bond_length_decrementer.get_value(), 1
        #     )
        #     return m

        # endoperoxide[1][0].add_updater(C_O_bond_updater)

        self.play(endoperoxide[3][3].animate.set_color(BLUE))

        describer_arrow = Arrow(ORIGIN, LEFT).next_to(
            endoperoxide[3][3], RIGHT, buff=0.35
        )

        describer_text = Text('Stretching of\noxygen bond\n(aka a "vibrational mode")')

        describer_text.scale(0.5).next_to(describer_arrow, RIGHT, buff=0.25)

        description = VGroup(
            describer_text,
            describer_arrow,
        ).add_background_rectangle()

        self.clouds = clouds = VGroup(
            ElectronCloud(endoperoxide[3][1]),
            ElectronCloud(endoperoxide[3][0]),
        )

        self.cloud_describer_arrow = Arrow(ORIGIN, RIGHT).next_to(
            self.clouds[0], LEFT, buff=SMALL_BUFF
        )
        self.cloud_describer_text = (
            Text("Delocalised\nelectrons")
            .scale(0.5)
            .add_background_rectangle()
            .next_to(self.cloud_describer_arrow, LEFT, buff=0)
        )

        self.description_cloud = description_cloud = VGroup(
            self.cloud_describer_text, self.cloud_describer_arrow
        )
        self.play(
            ShowCreation(description),
            ShowCreation(description_cloud),
        )

        # clouds[1].add_updater(lambda m: m.move_to(endoperoxide[3][0]))
        for _ in range(3):
            # self.play(
            #     bond_length_decrementer.animate.set_value(0.85),
            # )

            # self.play(bond_length_decrementer.animate.set_value(1.2))

            self.play(
                # AnimationGroup(
                ## This workaround works way better than I expected
                ApplyMethod(
                    endoperoxide[1][0].become,
                    endoperoxide[3][3]
                    .copy()
                    .clear_updaters()
                    .set_color(WHITE)
                    .next_to(endoperoxide[0][6], UP, buff=0),
                    rate_func=there_and_back,
                ),
                FadeInThenOut(clouds)
                # ),
            )

        self.play(
            FadeOut(description),
            FadeOut(description_cloud),
        )

        self.clear_endoperoxide_updaters()

    def add_endoperoxide_updaters(self):
        endoperoxide[3][1].add_updater(
            lambda m: m.next_to(endoperoxide[1][0], UP, buff=0.02)
        )

        endoperoxide[3][3].add_updater(
            lambda m: m.put_start_and_end_on(
                m.get_top(), endoperoxide[3][1].get_center() + UP * 0.2
            )
        )

    def clear_endoperoxide_updaters(self):
        endoperoxide[3][1].clear_updaters()
        endoperoxide[3][3].clear_updaters()
        endoperoxide[1][0].clear_updaters()


class ReasonsBehindChemiluminescenceSecondPart(ReasonsBehindChemiluminescence):
    # NOTE: Use -n 39 here
    def construct(self):
        super().construct()
        self.add_endoperoxide_updaters()
        self.clouds[0].shift(DOWN * 0.2)
        self.play(
            FadeIn(self.clouds),
            ApplyMethod(
                endoperoxide[1][0].become,
                endoperoxide[3][3]
                .copy()
                .clear_updaters()
                .set_color(WHITE)
                .next_to(endoperoxide[0][6], UP, buff=0),
            ),
            ShowCreation(self.description_cloud),
        )
        self.play(
            Transform(
                self.cloud_describer_text,
                Text("Localised\nelectrons")
                .scale(0.5)
                .next_to(self.cloud_describer_arrow, LEFT, buff=0)
                .add_background_rectangle(),
            ),
            self.clouds.animate.set_color(YELLOW)
        )
        self.add(get_submobject_index_labels(endoperoxide[0]))
        # self.wait()


class ElectronCloudTest(Scene):
    def construct(self):
        cloud = VGroup(Arc(0, TAU / 2), Polygon(LEFT, RIGHT, DOWN * 2)).set_fill(
            BLUE_B, 0.85
        )

        self.add(cloud)


class ElectronCloud(Dot):
    def __init__(
        self, atom: TexSymbol, color=BLUE, fill_opacity=0.35, radius=0.3, **kwargs
    ):
        super().__init__(
            atom.get_center(),
            color=color,
            fill_opacity=fill_opacity,
            radius=radius,
            **kwargs,
        )


class FadeInThenOut(Succession):
    def __init__(self, mobject: Union[Mobject, VMobject], run_time=1, **kwargs):
        super().__init__(
            FadeIn(mobject, run_time=run_time / 2),
            FadeOut(mobject, run_time=run_time / 2),
            **kwargs,
        )


