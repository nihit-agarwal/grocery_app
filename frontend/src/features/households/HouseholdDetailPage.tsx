import {
    Button,
    Card,
    Paper,
    Stack,
    Text,
    Title
} from "@mantine/core"
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { http } from "../../services/http";
import type { JSX } from "react/jsx-runtime";


function IsOwner({children, role} : {children: JSX.Element; role: string}) {
    return role === "owner" ? children : null;
}

export default function HouseholdDetailPage() {

    const { householdid } = useParams();
    const location = useLocation();

    const state = location.state as 
    | {
        householdId?: string;
        houseName?: string;
        role?: string;
        joinedAt?: string;

    }
    | undefined;
    const navigate = useNavigate();

    async function deleteHousehold() {

        try {
            await http.delete(`/households/${householdid}`);
            navigate("/households", { replace: true})
        } catch {
            console.log("Error! Cannot delete household")
        }
    }

    const householdId = state?.householdId ?? householdid ?? "";
    const householdName = state?.houseName ?? "Household";
    const householdRole = state?.role ?? "member";
    return (
        <main className="page">
            <Paper withBorder shadow="md" radius="xl" p="xl" maw={760} mx="auto">
                <Stack gap="lg">
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm">
                            Grocery App
                        </Text>
                        <Title order={1}> {householdName} </Title>
                        <Text c="dimmed">
                            Edit the inventory, cart, or catalog.
                        </Text>
                    </div>
                    
                    <IsOwner role={householdRole}>
                        <Stack gap="md" justify="flex-end" style={{ flexDirection: "row" }}>
                            <Button onClick={deleteHousehold} size="sm" radius="md" color="red">Delete</Button>    
                        </Stack>
                    </IsOwner>
                    


                    <Stack gap="md">
                        <Card
                        withBorder
                        radius="lg"
                        p="lg"
                        component={Link}
                        to={"/households/" + householdId + "/catalog"}
                        >
                            Catalog
                        </Card>

                        <Card
                        withBorder
                        radius="lg"
                        p="lg"
                        component={Link}
                        to={"/household/" + householdId + "/inventory"}
                        >
                            Inventory
                        </Card>

                        <Card
                        withBorder
                        radius="lg"
                        p="lg"
                        >
                            Cart
                        </Card>


                    </Stack>

                </Stack>
            </Paper>
        </main>
    )
}