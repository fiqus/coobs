<template>
    <div v-if="!hasPeriod || !hasActions" class="row">
        <div class="col-sm-4"></div>
        <div class="col-12 col-sm-4">
            <div class="mx-auto">
                <img src="images/Ilustracion_COOBS_home_01.png" class="w-100 img-fluid mb-3">
                <div v-if="!hasPeriod" class="row justify-content-center">
                    <h1 class="h4 text-center mb-3">{{$t("noPeriodsMessage")}}</h1>
                    <router-link class="btn btn-primary mb-3 mb-sm-0" :to="{name: 'period-edit', params: {periodId: 0}}">
                        {{$t("createPeriod")}}
                    </router-link>
                </div>
                <div v-else class="row justify-content-center">
                    <h1 class="h4 text-center mb-3">{{$t("emptyActionMsgForCurrentPeriod")}}</h1>
                    <router-link class="btn btn-primary mb-3 mb-sm-0" :to="{name: 'action-edit', params: {actionId: 0}}">
                        {{$t("createAction")}}
                    </router-link>
                </div>
            </div>
        </div>
        <div class="col-sm-4"></div>
    </div>
</template>

<script>
export default {
    props: {
        hasPeriod: {
            type: Boolean,
            default: false
        },
        hasActions: {
            type: Boolean,
            default: false
        }
    }
}
</script>
