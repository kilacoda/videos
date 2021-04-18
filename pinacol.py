from chanim import *
from math import degrees

config.tex_template = TexTemplateLibrary.simple


class ReferenceGrid(VMobject):
    """
    A grid meant to provide an easy reference for shifting and placing objects.
    Born out of my frequent need to manipulate ChemObjects which can be a real pain in
    the arse if eyeballed.
    """

    def __init__(self, axes_color=RED, **kwargs):
        super().__init__(**kwargs)

        self.vert_int_lines = VGroup(
            *[
                Line(
                    config.frame_y_radius * UP,
                    config.frame_y_radius * DOWN,
                )
                .shift(i * RIGHT)
                .set_opacity(0.5)
                for i in range(
                    int(-config.frame_x_radius), int(config.frame_x_radius) + 1
                )
            ]
        )

        self.vert_int_lines[int(config.frame_x_radius)].set_color(axes_color)

        self.vert_deci_lines = VGroup(
            *[
                Line(
                    config.frame_y_radius * UP,
                    config.frame_y_radius * DOWN,
                )
                .shift((i + j * 0.1) * RIGHT)
                .set_opacity(0.25)
                .set_stroke(width=0.85)
                for j in range(0, 11)
                for i in range(
                    int(-config.frame_x_radius), int(config.frame_x_radius) + 1
                )
            ]
        )

        self.horiz_int_lines = VGroup(
            *[
                Line(
                    config.frame_x_radius * LEFT,
                    config.frame_x_radius * RIGHT,
                )
                .shift(i * UP)
                .set_opacity(0.5)
                for i in range(
                    int(-config.frame_y_radius), int(config.frame_y_radius) + 1
                )
            ]
        )

        self.horiz_int_lines[int(config.frame_y_radius)].set_color(axes_color)

        self.horiz_deci_lines = VGroup(
            *[
                Line(
                    config.frame_x_radius * LEFT,
                    config.frame_x_radius * RIGHT,
                )
                .shift((i + j * 0.1) * UP)
                .set_opacity(0.25)
                .set_stroke(width=0.85)
                for j in range(0, 11)
                for i in range(
                    int(-config.frame_y_radius), int(config.frame_y_radius) + 1
                )
            ]
        )

        self.add(
            self.vert_deci_lines,
            self.horiz_deci_lines,
            self.vert_int_lines,
            self.horiz_int_lines,
        )


class PinacolRearrangementMechanism(Scene):
    def construct(self):
        ref_grid = ReferenceGrid()
        # self.play(
        #     ShowCreation(ref_grid, run_time=7, rate_func=rate_functions.ease_in_cubic)
        # )

        self.add(ref_grid)

        pinacol = ChemWithName(
            "H_3C-C(-[2]CH_3)(-[-2]\\Charge{0:1.25pt=\:,270:1.25pt=\:}{O}-[4]H)-C(-[2]CH_3)(-[-2]\\Charge{180:1.25pt=\:,270:1.25pt=\:}{O}H)-CH_3",
            "Pinacol",
        )

        self.play(pinacol.creation_anim())
        # self.wait(2)

        sulfurina = ChemObject("H-O-SO_3H").shift(DOWN * 3)

        self.play(FadeOutAndShift(pinacol.name, LEFT), FadeInFrom(sulfurina))
        # self.wait(2)

        self.play(sulfurina.animate.shift(2.075 * RIGHT + 1.3 * UP))
        ## Looks like the charge macro's going to be a PITA for this one...
        # print_family(pinacol.chem[0][26])
        # self.play(pinacol.chem[0][25].animate.set_color(YELLOW))
        # self.play(pinacol.chem[0][27].animate.next_to(pinacol.chem[0][26],DOWN, buff=0.15))

        pinacol.chem[0][26].set_opacity(0)

        dots = charge_to_dots(pinacol.chem[0][27])

        # self.play(
        #     pinacol.chem[0][27].animate.rotate(-90 * DEGREES).shift(DOWN * 0.1),
        # )
        # self.add(dots.copy().set_color(RED))
        # self.play(pinacol.chem[0][27][0].animate.shift(DOWN))

        ## hah, they'll never know... I've got the power of bad, hacky code on my side!
        pinacol.chem[0][26].become(dots[0])
        pinacol.chem[0][27].become(dots[1])

        oxy_elec_grp_1 = VGroup(
            pinacol.chem[0][26],
            pinacol.chem[0][27],
        )

        self.play(
            Rotate(oxy_elec_grp_1, PI / 2),
        )

        self.play(
            oxy_elec_grp_1.animate.shift(DOWN * 0.1),
        )

        # self.wait()

        # self.add(index_labels(sulfurina[0]))

        self.play(
            Transform(
                sulfurina[0][2], ElectronPair(pair_buff=0.1).move_to(sulfurina[0][2])
            )
        )

        OH_bond = (
            Line(start=pinacol.chem[0][26], end=pinacol.chem[0][27])
            .match_style(pinacol.chem[0][29])
            .stretch_to_fit_height(0.3)
        )

        self.play(
            sulfurina[0][2].animate.next_to(sulfurina[0][1], UP, buff=0.125),
            FadeOut(oxy_elec_grp_1),
            ShowCreation(OH_bond),
        )
        self.wait()

        # h2_grp = VGroup(sulfurina[0][0], pinacol.chem[0][28])
        h2 = (
            ChemObject("H_2")
            .move_to(pinacol.chem[0][28])
            .shift(DOWN * 0.03 + RIGHT * 0.1)
        )

        self.play(
            Transform(pinacol.chem[0][28], h2),
            Transform(OH_bond, MathTex("\\oplus").move_to(OH_bond)),
            FadeOutAndShift(
                VGroup(
                    sulfurina[0][1],
                    sulfurina[0][2],
                    sulfurina[0][3],
                    sulfurina[0][4],
                    sulfurina[0][5],
                    sulfurina[0][6],
                    sulfurina[0][7],
                ),
                RIGHT,
            ),
            FadeOutAndShift(
                sulfurina[0][0],
                pinacol.chem[0][28].get_center() - sulfurina[0][0].get_center(),
            ),
        )

        self.play(
            Transform(
                pinacol.chem[0][29],
                ElectronPair().rotate(PI / 2).move_to(pinacol.chem[0][29]),
            )
        )

        carbcation_indicator = (
            MathTex("\\oplus")
            .next_to(pinacol.chem[0][17], DOWN, buff=0.1)
            .shift(LEFT * 0.3 + UP * 0.1)
        )

        self.play(
            pinacol.chem[0][29]
            .animate.rotate(PI / 2)
            .next_to(pinacol.chem[0][23], UP, buff=0.1),
            ShowCreation(carbcation_indicator),
            Uncreate(OH_bond),
        )
        # self.add(
        #     index_labels(pinacol.chem[0]).set_color(YELLOW),
        #     index_labels(sulfurina[0]).set_color(RED),
        # )
        self.wait()

        leaving_water = VGroup(
            pinacol.chem[0][23],
            pinacol.chem[0][24],
            pinacol.chem[0][25],
            # pinacol.chem[0][26],
            # pinacol.chem[0][27],
            pinacol.chem[0][28],
            pinacol.chem[0][29],
            # sulfurina[0][0],
        )
        self.play(
            Transform(
                leaving_water,
                ChemObject("H_2 \\charge{45=\\:,315=\\:}{O}")
                .move_to(leaving_water)
                .shift(DOWN),
            ),
        )

        self.wait()

        self.play(
            leaving_water.animate.shift(DOWN * 3),
        )

        
        # self.play(
        # Transform(pinacol.chem[0][26], dots[0]),
        # Transform(pinacol.chem[0][27], dots[1])
        # )
        # self.add(index_labels(pinacol.chem[0][27][0]))
        # print_family(pinacol.chem[0][27])
        # self.play(pinacol.chem[0][27].animate.stretch_to_fit_height(0.5))

        # ReplacementTransform(pinacol.chem[0][27], charge_to_dots(pinacol.chem[0][27]))
        # dot_grp_1 = charge_to_dots(pinacol.chem[0][27]).set_color(YELLOW)
        # # self.remove(pinacol.chem[0][27])
        # self.add(dot_grp_1)
        # print_family(pinacol.chem[0][27])
        # print_family(pinacol.chem[0][25])
        # self.add(index_labels(pinacol.chem[0]))

        # self.play(
        # ApplyMethod(pinacol.chem[0][27].shift,DOWN, rate_func=there_and_back)
        # )


## aah frick.
def charge_to_dots(charge: TexSymbol):
    """
    Made to get around the problems caused by `chemfig`'s new `\charge` macro.
    Apparently, manim doesn't convert both the dots rendered through this macro to
    individual Dot/Circle/whatever objects, making it virtually impossible to separate them
    like before (for some odd reason...). Till a more permanent fix is found,
    consider silently `Transform`ing your charge sybols into the `Dot` VGroup spit out
    by this function.
    """
    charge_copy = (
        charge.copy()
    )  ## Will be rotated such that it's perpendicular to the x-axis
    # arrange_direction = normalize(rotate_vector(charge_copy.get_center(), 90 * DEGREES))

    arrange_direction = normalize(charge_copy.get_end() - charge_copy.get_start())

    ## Debug stuff
    # console.print(f"{charge_copy.get_center()=}")
    # console.print(f"{charge_copy.points=}")
    # console.print(f"{charge.get_center()=}")
    # console.print(f"{charge.points=}")
    # console.print(f"{charge_copy.get_start()=}")
    # console.print(f"{charge.get_start()=}")
    console.print(f"{degrees(angle_of_vector(charge_copy.get_center()))=}")
    console.print(arrange_direction)
    console.print(
        f"Angle of arrange_direction = {degrees(angle_of_vector(arrange_direction))}"
    )
    console.print(degrees(90 * DEGREES - angle_of_vector(arrange_direction)))

    charge_copy.rotate(
        90 * DEGREES - angle_of_vector(arrange_direction)
    )  ## Amount to be rotated by to get back to normal position

    buff_line = Line(
        ## yes, I'm VERY pedantic about this stuff.
        start=charge_copy.get_bottom() + 0.0325 * UP,
        end=charge_copy.get_top() + 0.0325 * DOWN,
    )  ## line of distance between dot centers, makes it much easier to arrange the dots as required.

    buff = buff_line.get_length() / 2

    ## More debug stuff...
    console.print(f"{buff=}")
    console.print(-arrange_direction * (buff))

    # scale factor determined via trial and error.
    dots = VGroup(Dot().scale(0.55), Dot().scale(0.55))

    # shift each individual dot do the position of the original dot
    dots[0].shift(-arrange_direction * buff)
    dots[1].shift(arrange_direction * buff)

    dots.buff = buff
    # dots.add(buff_line, charge_copy)
    dots.move_to(charge)

    return dots


class TestCharge(Scene):
    def construct(self):
        self.camera.background_color = GREEN
        charge = ChemObject("\\charge{[:sep=1.5em]0=\:}{}")
        test_dot = Dot().scale(0.55).set_color(YELLOW).set_opacity(0)

        # self.add(
        #     charge,
        #     test_dot,
        #     Line(
        #         start=charge.get_bottom() + 0.025 * UP,
        #         end=charge.get_top() + 0.025 * DOWN,
        #         color=RED,
        #     ),
        # )

        dots_from_charge = charge_to_dots(charge[0][0])

        self.add(
            charge.set_color(RED),
            dots_from_charge[0].set_color(YELLOW),
            # dots_from_charge[1].set_color(BLUE),
        )

        # self.wait()


class FuckYouChemfig(Scene):
    def construct(self):
        mob = VMobject()
        mob.current_path_start = np.zeros((1, mob.dim))
        start_point = mob.points[-1] if mob.points.shape[0] else np.zeros((1, self.dim))

        mob.start_new_path([173.351648, 6.82813, 0.0])

        mob.add_cubic_bezier_curve_to(
            [
                [172.996179, 6.82813, 0.0],
                [172.707117, 7.11328, 0.0],
                [172.707117, 7.46875, 0.0],
            ]
        )
        print(mob.current_path_start, mob.points)

