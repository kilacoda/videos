from typing import Iterable
from chanim import *


def overlap_exists(
    mob1: VMobject, mob2: VMobject, tolerance=0.5, check_all_submobs=False
):
    if not check_all_submobs:
        return abs(get_norm(mob1.get_center() - mob2.get_center())) < tolerance
    else:
        return any(
            [
                get_norm(item1.get_center() - item2.get_center()) < tolerance
                for item1 in mob1
                for item2 in mob2
            ]
        )


def Range(in_val, end_val, step=1):
    return list(np.arange(in_val, end_val + step, step))


class TestScene(Scene):
    # CONFIG = {"dx": 0.005}
    dx = 0.005

    def get_coord_from_proportion(self, vmob, proportion):
        return vmob.point_from_proportion(proportion)

    def construct(self):
        circle1 = ChemObject(Benzene)
        circle2 = ChemObject(Benzene)

        g_circles = VGroup(circle1, circle2).arrange(RIGHT, buff=-0.5)

        self.add(g_circles)
        intersections = self.get_intersections_between_two_vmobs(circle1[0], circle2[0])
        print(*intersections)
        for point in intersections:
            self.add(Dot(radius=0.05).move_to(point))

    def get_points_from_curve(self, vmob):
        coords = []
        for point in Range(0, 1, self.dx):
            dot = Dot(self.get_coord_from_proportion(vmob, point))
            coords.append(dot.get_center())
        return coords

    def get_intersections_between_two_vmobs(
        self,
        vmob1,
        vmob2,
        tolerance=0.05,
        radius_error=0.2,
        use_average=True,
        use_first_vmob_reference=False,
    ):
        coords_1 = self.get_points_from_curve(vmob1)
        coords_2 = self.get_points_from_curve(vmob2)
        intersections = []
        for coord_1 in coords_1:
            for coord_2 in coords_2:
                distance_between_points = get_norm(coord_1 - coord_2)
                if use_average:
                    coord_3 = (coord_2 - coord_1) / 2
                    average_point = coord_1 + coord_3
                else:
                    if use_first_vmob_reference:
                        average_point = coord_1
                    else:
                        average_point = coord_2
                if len(intersections) > 0 and distance_between_points < tolerance:
                    last_intersection = intersections[-1]
                    distance_between_previus_point = get_norm(
                        average_point - last_intersection
                    )
                    if distance_between_previus_point > radius_error:
                        intersections.append(average_point)
                if len(intersections) == 0 and distance_between_points < tolerance:
                    intersections.append(average_point)
        return intersections


class OverlapTest(Scene):
    def construct(self):
        c1 = Circle(color=random_color()).shift(LEFT / 2)
        c2 = Circle(color=random_color()).shift(RIGHT / 2)

        overlap_exists(c1, c2)
        self.add(c1, c2, ArcPolygon())


class Polymer(VMobject):
    def __init__(
        self,
        base_unit: Union[str, ChemObject],
        repetition_indices: Iterable[int] = None,
        num_repetitions: int = None,
        include_base: bool = True,
        _overlap_check_tolerance=0.05,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._overlap_check_tolerance = _overlap_check_tolerance
        self.base_unit = base_unit = (
            ChemObject(base_unit) if type(base_unit) == str else base_unit
        )

        if include_base:
            self.add(base_unit)

        self.start_index = 1 if include_base else 0

        if repetition_indices is None:
            self.repetition_indices = repetition_indices = [0, len(base_unit[0]) - 1]

        increment = 1

        if num_repetitions is None:
            self.num_repetitions = num_repetitions = len(repetition_indices)
        # self.add(index_labels(base_unit[0]))
        self.reps_done: int = 0
        if num_repetitions > len(repetition_indices):
            rounds_done: int = self.reps_done // increment
            # self.repeatable_bases = self.submobjects
            # base_groups = [[base_unit]]
            # current_group_index = 0
            # curr_mob = base_groups[0][0]
            curr_mob = base_unit
            curr_index = self.start_index

            while self.reps_done < num_repetitions:
                # print(f"{len(self.submobjects)=}\n")
                # if curr_mob == base_unit:
                for index in repetition_indices:
                    # print(f"{self.reps_done=}")
                    # curr_mob.set_color(random_color())
                    self.add_repetition(curr_mob, index)
                    # curr_mob.set_color(WHITE)
                    # else:
                    # for index in repetition_indices:
                    #     self.add_repetition(curr_mob, index)
                    #     self.reps_done += 1
                    #     curr_index += 1
                    #     curr_mob = self[curr_index]
                self.start_index += increment
                # print_family(self)
                # print(len(self))
                # print(self.start_index - 1)
                curr_mob = self[self.start_index - 1]
                # print_family(curr_mob)
                # print(f"{len(self.repeatable_bases)=}\n")
                # print(f"{(self.reps_done<num_repetitions)=}\n")
                # curr_mob.set_color(random_color())
                # if curr_mob == base_unit:
                #     self.add_repetitions(curr_mob, repetition_indices)
                #     self.reps_done += len(repetition_indices)
                # else:
                #     self.add_repetitions(
                #         curr_mob,
                #         [repetition_indices[self.reps_done % len(repetition_indices)]],
                #     )
                #     self.reps_done += 1
                # base_groups.append(self.repeatable_bases.copy())
                # self.repeatable_bases.clear()
                # current_group_index += 1
                # print(f"{base_groups=}")
                # # repeatable_bases.append(self[-1])
                # print(f"{self.reps_done=}\n")

                # curr_mob = (
                #     base_groups[current_group_index][
                #         -(self.reps_done % len(repetition_indices))
                #     ]
                #     if self.reps_done > 0
                #     else base_unit
                # )

        elif num_repetitions <= len(repetition_indices):
            indices = repetition_indices[:num_repetitions]
            for index in repetition_indices:
                self.add_repetition(base_unit, index)

    def add_repetition(
        self, mob_or_index: Union[ChemObject, int], repetition_index: int
    ):
        base_unit = self[mob_or_index] if type(mob_or_index) == int else mob_or_index

        # self.add(index_labels(base_unit[0]).set_color(random_color()))
        # print(f"{repetition_indices=}\n")
        # for i in repetition_indices:
        temp_base_unit_copy = base_unit.copy()
        temp_base_unit_copy.move_to(base_unit[0][repetition_index])
        print(
            overlap_exists(temp_base_unit_copy[0], base_unit[0], check_all_submobs=True)
        )
        while overlap_exists(
            temp_base_unit_copy[0], base_unit[0], check_all_submobs=True
        ):
            temp_base_unit_copy.shift(
                (
                    get_norm(
                        temp_base_unit_copy.get_left()
                        - temp_base_unit_copy.get_center()
                    )
                )
                * normalize(
                    base_unit[0][repetition_index].get_center() - base_unit.get_center()
                )
                * 0.02
            )

        for item in self:
            # print(overlap_exists(item, temp_base_unit_copy, self._overlap_check_tolerance))
            if overlap_exists(item, temp_base_unit_copy, self._overlap_check_tolerance):
                # ) or overlap_exists(item, self.base_unit, self._overlap_check_tolerance):
                del temp_base_unit_copy
                return
        # self.repeatable_bases.append(temp_base_unit_copy)

        self.add(temp_base_unit_copy)
        self.reps_done += 1


class PolymerTest(Scene):
    def construct(self):
        chem = ChemObject(Benzene)
        # self.add(chem,index_labels(chem[0]))
        p = Polymer(
            chem, [0, 1, 3, 4, 6, 7], num_repetitions=135, include_base=True
        ).scale(0.85)

        # self.add(
        #     chem,
        #     #  index_labels(chem[0])
        # )
        # for m in p:
        #     self.play(Write(m))
        #     self.wait(0.5)
        # self.play(FadeIn(index_labels(p)))
        for m in p:
            self.play(
                m.animate(rate_func=there_and_back, run_time=0.1).set_color(YELLOW)
            )
        # self.add(p, index_labels(p))


class PolymerTest2(Scene):
    def construct(self):
        c = ChemObject("-CH=CH")
        # print(c[0][2].width)
        # c[0][2].stretch_to_fit_width(0.35).shift(RIGHT * 0.35)
        # self.add(c, index_labels(c[0]))
        p = Polymer(c, [2, 4], 4)

        self.add(p)

class PolymerTest3(Scene):
    def construct(self):
        neoprene = ChemObject("-CH_2-C(-[-2]Cl)=CH-CH_2")
        # self.add(neoprene, index_labels(neoprene[0]))
        p = Polymer(neoprene,[3,14],_overlap_check_tolerance=1.75)

        self.play(Write(p))
        self.wait()


class HindiTest(Scene):
    def construct(self):
        text = Text("नमस्ते, मेरा नाम राघव है।", font="Karma")

        self.play(Write(text))
        self.wait()