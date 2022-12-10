class Position(object):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        return f"(x={self.x}, y={self.y})"

    def as_coordinates(self):
        return (self.x, self.y)


class Movable(Position):
    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def move_up(self):
        self.y += 1

    def move_down(self):
        self.y -= 1

    def move(self, direction: str):
        if direction == "R":
            self.move_right()
        elif direction == "L":
            self.move_left()
        elif direction == "U":
            self.move_up()
        elif direction == "D":
            self.move_down()

    def move_horizontally(self, direction: int):
        if direction > 0:
            self.move_right()
        elif direction < 0:
            self.move_left()

    def move_vertically(self, direction: int):
        if direction > 0:
            self.move_up()
        elif direction < 0:
            self.move_down()

    def follow(self, other: Position):
        x_direction = other.x - self.x
        x_dist = abs(x_direction)
        y_direction = other.y - self.y
        y_dist = abs(y_direction)

        if x_dist >= 1 and y_dist > 1 or y_dist >= 1 and x_dist > 1:
            # diagonal move
            self.move_horizontally(x_direction)
            self.move_vertically(y_direction)
            print("moving diagonally")
        elif y_dist == 0 and x_dist > 1:
            self.move_horizontally(x_direction)
        elif x_dist == 0 and y_dist > 1:
            self.move_vertically(y_direction)
        elif x_dist > 2 or y_dist > 2:
            raise Exception(
                f"current distance to big ({self.as_coordinates()}) vs ({other.as_coordinates()})"
            )


class RopeKnot(Movable):
    def __init__(self, x: int, y: int, id: int = 0) -> None:
        super().__init__(x, y)
        self.next_knot = None
        self.id = id

    def __str__(self):
        next_id = self.next_knot.id if self.next_knot else None
        return f"RopeKnot(x={self.x}, y={self.y}, id={self.id}, next={next_id})"

    def set_connection(self, other: "RopeKnot"):
        self.next_knot = other

    def move(self, direction: str):
        super().move(direction)
        knot = self
        while knot:
            if knot.next_knot:
                try:
                    knot.next_knot.follow(knot)
                except Exception as e:
                    raise Exception(f"Ids {knot.id} - {knot.next_knot.id}: {e}")
            knot = knot.next_knot

    def update_connected(self):
        self.next_knot.follow(self)


class Rope(object):
    def __init__(self, start_x: int, start_y: int, knots: int):
        self.head = RopeKnot(x=start_x, y=start_y, id=0)
        self.__setup_knots(start_x=start_x, start_y=start_y, knots=knots - 1)

    def __setup_knots(self, start_x: int, start_y: int, knots: int):
        prev_knot = self.head
        for i in range(knots):
            next_knot = RopeKnot(x=start_x, y=start_y, id=i + 1)
            prev_knot.set_connection(next_knot)
            prev_knot = next_knot

    def __str__(self) -> str:
        output = []
        knot = self.head
        while knot:
            output.append(str(knot))
            knot = knot.next_knot
        return "\n".join(output)

    def move(self, direction: str):
        self.head.move(direction=direction)

    def get_tail_coordinates(self) -> tuple[int, int]:
        tail = self.head
        counter = 0
        while tail.next_knot:
            tail = tail.next_knot
            counter += 1
        return tail.as_coordinates()


def parse_input_part1(input):
    head = Movable(x=0, y=0)
    tail = Movable(x=0, y=0)

    tail_locations: list[tuple[int, int]] = [tail.as_coordinates()]
    head_locations: list[tuple[int, int]] = [head.as_coordinates()]

    for line in input:
        direction, count = line.strip().split(" ")

        for step in range(int(count)):
            head.move(direction=direction)
            tail.follow(head)
            head_locations.append(head.as_coordinates())
            tail_locations.append(tail.as_coordinates())

    return head_locations, tail_locations


def parse_input_part1_v2(input):
    rope = Rope(start_x=0, start_y=0, knots=2)
    tail_locations: list[tuple[int, int]] = [rope.get_tail_coordinates()]
    head_locations: list[tuple[int, int]] = [rope.head.as_coordinates()]

    for line in input:
        direction, count = line.strip().split(" ")
        for step in range(int(count)):
            rope.move(direction=direction)
            head_locations.append(rope.head.as_coordinates())
            tail_locations.append(rope.get_tail_coordinates())

    return head_locations, tail_locations


def parse_input_part2(input):

    rope = Rope(start_x=0, start_y=0, knots=10)
    print(rope)
    tail_locations: list[tuple[int, int]] = [rope.get_tail_coordinates()]
    head_locations: list[tuple[int, int]] = [rope.head.as_coordinates()]

    for line in input:
        direction, count = line.strip().split(" ")
        for step in range(int(count)):
            rope.move(direction=direction)
            head_locations.append(rope.head.as_coordinates())
            tail_locations.append(rope.get_tail_coordinates())

    return head_locations, tail_locations


def main():
    with open("input.txt", "r") as input:
        head_locations, tail_locations = parse_input_part1(input)

        tail_unique_locations = list(set(tail_locations))

        print(f"Part 1: {len(tail_unique_locations)}")

    with open("input.txt", "r") as input:
        part2_head_locations, part2_tail_locations = parse_input_part2(input)

        part2_tail_unique_locations = list(set(part2_tail_locations))
        print(f"Part 2: {len(part2_tail_unique_locations)}")


if __name__ == "__main__":
    main()
